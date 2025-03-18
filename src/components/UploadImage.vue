<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card shadow">
          <!-- Header -->
          <div class="card-header bg-gradient text-white p-4" 
               style="background: linear-gradient(to right, #0d6efd, #0b5ed7)">
            <div class="d-flex align-items-center">
              <i class="bi bi-file-text fs-4 me-2"></i>
              <div>
                <h3 class="mb-1">Receipt Scanner</h3>
                <p class="mb-0 text-light opacity-75">Upload your receipt to extract data automatically</p>
              </div>
            </div>
          </div>

          <div class="card-body p-4">
            <!-- Upload Area -->
            <div 
              class="upload-area p-5 mb-4 rounded-3 text-center position-relative"
              :class="{
                'border-primary bg-light': isDragging,
                'border-success bg-success bg-opacity-10': selectedFile,
                'border-secondary': !isDragging && !selectedFile
              }"
              @drop.prevent="handleDrop"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
            >
              <input
                type="file"
                class="d-none"
                ref="fileInput"
                @change="handleFileUpload"
                accept="image/*"
                id="imageUpload"
              />
              
              <label for="imageUpload" class="cursor-pointer">
                <i 
                  class="bi"
                  :class="selectedFile ? 'bi-check-circle text-success' : 'bi-upload text-primary'"
                  style="font-size: 3rem"
                ></i>
                
                <h5 class="mt-3">
                  {{ selectedFile ? selectedFile.name : 'Drag & drop your receipt or click to browse' }}
                </h5>
                <p class="text-muted mb-0">
                  {{ selectedFile ? 'Click upload button below to process' : 'Supported formats: JPG, PNG, PDF' }}
                </p>
              </label>
            </div>

            <!-- Upload Button -->
            <div class="text-center mb-4">
              <button
                class="btn btn-primary btn-lg px-5 rounded-pill"
                @click="submitFile"
                :disabled="!selectedFile || loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Processing...' : 'Process Receipt' }}
              </button>
            </div>

            <!-- Error Alert -->
            <div 
              v-if="error" 
              class="alert alert-danger alert-dismissible fade show" 
              role="alert"
            >
              <i class="bi bi-exclamation-circle-fill me-2"></i>
              {{ error }}
              <button type="button" class="btn-close" @click="error = null"></button>
            </div>

            <!-- Results Section -->
            <div v-if="result" class="mt-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Extracted Data</h4>
                <button 
                  class="btn btn-success"
                  @click="downloadJson"
                >
                  <i class="bi bi-download me-2"></i>
                  Download JSON
                </button>
              </div>

              <div class="bg-light rounded-3 p-4 border">
                <!-- Basic Info -->
                <div class="row mb-4">
                  <div class="col-md-3 mb-3">
                    <label class="text-muted small">Store Name</label>
                    <div class="fw-medium">{{ result.store_name || 'N/A' }}</div>
                  </div>
                  <div class="col-md-3 mb-3">
                    <label class="text-muted small">Date & Time</label>
                    <div class="fw-medium">{{ result.date_time || 'N/A' }}</div>
                  </div>
                  <div class="col-md-3 mb-3">
                    <label class="text-muted small">Receipt Number</label>
                    <div class="fw-medium">{{ result.receipt_number || 'N/A' }}</div>
                  </div>
                  <div class="col-md-3 mb-3">
                    <label class="text-muted small">Total Amount</label>
                    <div class="fw-medium">{{ result.total || 'N/A' }}</div>
                  </div>
                </div>

                <!-- Items Table -->
                <div>
                  <label class="text-muted small mb-2">Items</label>
                  <div class="table-responsive" style="max-height: 300px;">
                    <table class="table table-sm table-hover mb-0">
                      <thead class="table-light sticky-top">
                        <tr>
                          <th>Item</th>
                          <th class="text-end">Price</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(item, index) in result.items" :key="index">
                          <td>{{ item.item_name }}</td>
                          <td class="text-end">{{ item.price }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      result: null,
      loading: false,
      error: null,
      isDragging: false
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.error = null;
      }
    },
    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;
        this.error = null;
      } else {
        this.error = 'Please upload an image file';
      }
    },
    async submitFile() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        const originalResult = response.data;
        this.result = {
          store_name: originalResult.store_name || "",
          date_time: originalResult.date_time || "",
          receipt_number: originalResult.receipt_number || "",
          items: originalResult.items || [],
          vat: originalResult.vat || "",
          total: originalResult.total || "",
        };
      } catch (err) {
        this.error = "Failed to process the image. Please try again.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    downloadJson() {
      if (!this.result) return;
      
      const jsonString = JSON.stringify(this.result, null, 2);
      const blob = new Blob([jsonString], { type: "application/json" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${this.result.store_name || 'receipt'}.json`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    }
  }
};
</script>

<style scoped>
.upload-area {
  border: 2px dashed #dee2e6;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: #0d6efd;
  background-color: rgba(13, 110, 253, 0.05);
}

.cursor-pointer {
  cursor: pointer;
}

/* Ensure the sticky header works in the table */
.table-responsive {
  overflow-y: auto;
}

.sticky-top {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: #f8f9fa;
}
</style>
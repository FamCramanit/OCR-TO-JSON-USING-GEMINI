<template>
  <div class="container mt-2">
    <div
      v-if="alertMessage != ''"
      :class="['alert', alertClass]"
      role="alert"
    >
    <i :class="['icon', iconAlert]"></i> {{ alertMessage }}
    </div>
    <div class="row">
      <div class="col-md-12 mb-4">
        <div class="card">
          <div
            class="card-header bg-dark text-white d-flex justify-content-between align-items-center"
          >
            <h5 class="mb-0">Upload Receipt</h5>
            <div class="form-check form-switch">
              <input
                class="form-check-input cursor-pointer" style="cursor:pointer;"
                type="checkbox"
                role="switch"
                v-model="autoSaveSwitch"
              />
              <label
                class="form-check-label text-light"
                style="font-size: 12px;"
                for="autoSaveSwitch"
                >Auto Save</label
              >
            </div>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <div
  class="upload-area mb-4"
  @dragover.prevent="dragOver"
  @dragleave.prevent="dragLeave"
  @drop.prevent="handleDrop"
  :class="{ dragging: isDragging }"
>
  <input
    type="file"
    ref="fileInput"
    class="d-none"
    @change="handleFileUpload"
    accept="image/*,application/pdf"
  />

  <!-- Show preview for images -->
  <div v-if="previewUrl" class="preview-in-upload">
    <img
      :src="previewUrl"
      class="img-fluid rounded"
      alt="Receipt preview"
    />
    <div class="preview-controls">
                      <button
                        @click.stop="removeFile"
                        class="btn btn-danger btn-sm"
                      >
                        <i class="bi bi-trash me-1"></i>Delete
                      </button>
                    </div>
  </div>

  <!-- Show preview for PDFs -->
  <div v-if="pdfPreview" class="preview-in-upload">
    <iframe
      :src="pdfPreview"
      class="pdf-preview"
    ></iframe>
    <div class="preview-controls">
                      <button
                        @click.stop="removeFile"
                        class="btn btn-danger btn-sm"
                      >
                        <i class="bi bi-trash me-1"></i>Delete
                      </button>
                    </div>
  </div>


  <!-- Show upload interface if no file -->
  <div v-if="!pdfPreview&&!previewUrl" class="text-center py-5">
    <i class="bi bi-cloud-upload fs-1"></i>
    <h5 class="mt-3">
      Drag a file here or click to select a file.
    </h5>
    <p class="text-muted mb-0">
      Supports images (JPG, PNG) and PDFs.
    </p>
    <button
      @click="$refs.fileInput.click()"
      class="btn btn-outline-dark btn-sm mt-3"
    >
      <i class="bi bi-image me-2"></i>Select file
    </button>
  </div>
</div>

              </div>

              <div class="col-md-6">
                <div class="card mb-4">
                  <div
                    class="card-header bg-dark text-white d-flex justify-content-between align-items-center"
                  >
                    <h5 class="mb-0">Result JSON</h5>
                    <div>
                      
                      <button
                        @click="copyJSON"
                        class="btn btn-secondary btn-sm me-2"
                        v-if="result && !loading"
                      >
                        <i class="bi bi-clipboard me-1"></i> Copy JSON
                      </button>
                      <button
                        @click="downloadJson"
                        class="btn btn-success btn-sm"
                        v-if="result && !loading"
                      >
                        <i class="bi bi-download me-1"></i> Download JSON
                      </button>
                    </div>
                  </div>
                  <div class="card-body">
                    <div v-if="loading" class="text-center py-5">
                      <div class="spinner-border text-success"></div>
                      <p class="mt-3">Processing...</p>
                    </div>
                    <p v-else-if="!result" class="text-muted text-center py-3">
                      There is no information.
                    </p>
                    
                    <pre v-if="result && !loading" class="json-result">{{
                      formatJSON(result)
                    }}</pre>
                  </div>
                </div>
              </div>
            </div>

            <div class="text-center my-2">
              <button
                @click="submitFile"
                class="btn btn-dark btn-sm fw-medium"
                :disabled="!selectedFile || loading"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                <i v-else class="bi bi-magic me-1"></i>
                {{ loading ? "Processing..." : "CONVERT" }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-12">
        <div class="card">
          <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Receipt information</h5>
            <div class="">
        <button
                        @click="toggleEditMode"
                        class="btn btn-sm me-2 py-1" :class="isEditing ? 'btn-primary' : 'btn-warning'"
                        v-if="result && !loading"
                      >
                        <i
                          class="me-1 bi"
                          :class="isEditing ? 'bi-check-circle' : 'bi-pencil'"
                        ></i>
                        {{ isEditing ? "Save" : "Edit" }}
                      </button>
                      <button
                        @click="cancle_edit"
                        class="btn btn-danger btn-sm me-2"
                        v-if="result && !loading && isEditing"
                      >
                        <i
                          class="bi"
                          :class="isEditing ? 'bi bi-x-lg' : ''"
                        ></i>
                        {{ isEditing ? "Cancle" : "" }}
                      </button>
      </div>
          </div>
  <div class="card-body">
    <div v-if="result && !loading">


      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title fw-bold">ข้อมูลร้านค้า</h5>
              <hr class="mb-1 mt-0" />
              <p class="mb-1">
                <strong>ชื่อร้าน:</strong>
                <input v-model="result.store_name" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" />
              </p>
              <p class="mb-1">
                <strong>วันที่:</strong>
                <input type="date" v-model="result.date_time" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" />
              </p>
              <p class="mb-1">
                <strong>เลขที่ใบเสร็จ:</strong>
                <input v-model="result.receipt_number" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" disabled />
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title fw-bold">สรุปยอดเงิน</h5>
              <hr class="mb-1 mt-0" />
              <p class="mb-1">
                <strong>ภาษีมูลค่าเพิ่ม:</strong>
                <input v-model="result.vat" type="number" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" />
              </p>
              <p class="mb-1">
                <strong>ยอดรวมทั้งสิ้น:</strong>
                <input v-model="result.total" type="number" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" disabled/>
              </p>
            </div>
          </div>
        </div>
      </div>
      <hr />
      <h5 class="fw-bold">รายการ</h5>
      <div class="table-responsive">
        <table class="table">
          <thead class="table-dark">
            <tr>
              <th class="text-center">ลำดับ</th>
              <th>รายการ</th>
              <th class="text-center">จำนวน</th>
              <th class="text-end">ราคาต่อหน่วย</th>
              <th class="text-end">รวม</th>
              <th class="text-center" v-if="isEditing">
                              ลบ
                            </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in result.items" :key="index">
              <td class="text-center">{{ index + 1 }}</td>
              <td><input v-model="item.item_name" :class="`form-control ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" /></td>
              <td class="text-center">
                <input v-model.number="item.quantity" type="number" :class="`form-control text-center ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" />
              </td>
              <td class="text-end">
                <input v-model.number="item.price" type="number" step="0.01" :class="`form-control text-end ${!isEditing ? 'bg-light border-0' : ''}`" :disabled="!isEditing" />
              </td>
              <td class="text-end">
                {{ formatPrice(item.price * (item.quantity || 1)) }}
              </td>
              <td class="text-center" v-if="isEditing">
                              <button
                                class="btn btn-danger btn-sm"
                                @click="removeItem(index)"
                                :disabled="!isEditing"
                              >
                                <i class="bi bi-trash"></i>
                              </button>
                            </td>
            </tr>
          </tbody>
        </table>
        <div v-if="isEditing" class="text-center">
                        <button
                          class="btn btn-primary btn-sm"
                          @click="addItem"
                          :disabled="!isEditing"
                        >
                          <i class="bi bi-plus-circle me-1"></i>Add Item
                        </button>
                      </div>
      </div>
    </div>
    <div v-if="!loading && !result" class="text-center text-secondary py-5">
      <p class="mt-3">There is no information.</p>
    </div>
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-3">Processing...</p>
    </div>
  </div>

        </div>
      </div>
    </div>
    <div v-if="isDownloading||downloadComplete" class="position-fixed border bg-light p-4 rounded d-flex progress_download">
      <div v-if="isDownloading" style="width: 100%;">
      <p class="fw-medium">Downloading...</p>
      <div class="progress">
        <div class="progress-bar" role="progressbar" :style="{ width: progress + '%' }" 
          :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
        </div>
      </div>
    </div>
    <p v-if="downloadComplete" class="text-success text-center mt-3 fw-medium" style="width: 100%;"><i class="bi bi-patch-check-fill me-2"></i>Download Success!</p>
</div>
    <span>{{ rawOcrText }}</span>
  </div>
  
</template>

<script>
import axios from "axios";

export default {
  name: "ReceiptUpload",
  data() {
    return {
      selectedFile: null,
      previewUrl: null,
      pdfPreview: null,
      result: null,
      loading: false,
      error: null,
      alertMessage: "", // ข้อความแจ้งเตือน
      alertClass: "", // คลาสของ Alert (success, danger, warning, etc.)
      isDragging: false,
      rawOcrText: null,
      isEditing: false,
      autoSaveSwitch: true,
      JsonEdit: null,
      isDownloading: false,
      progress: 0,
      downloadComplete: false,
    };
  },
  methods: {
    //  data_test() {
    //    this.result = {
    //        store_name: "CPB SOFTWARE (GERMANY) GMBH",
    //        date_time: "2024-03-01",
    //        receipt_number: "123100401",
    //        items: [
    //  {
    //    item_name: "Basic Fee wmView",
    //    price: 130,
    //    quantity: 1
    //  },
    //  {
    //    item_name: "Basis fee for additional user accounts",
    //    price: 10,
    //    quantity: 0
    //  },],
    //    total: 453.53,
    //    vat: 72.41
    //      };
      
    //  }
    //  ,
    cancle_edit() {
      this.isEditing = !this.isEditing;
    }
    ,
    dragOver() {
      this.isDragging = true;
    },
    dragLeave() {
      this.isDragging = false;
    },
    handleDrop(e) {
  this.isDragging = false;
  const file = e.dataTransfer.files[0];
  if (file && (file.type.startsWith("image/") || file.type === "application/pdf")) {
    this.handleFile(file);
  } else {
    this.error = "กรุณาอัพโหลดไฟล์รูปภาพหรือ PDF เท่านั้น";
  }
}
,
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleFile(file);
      }
    },
    handleFile(file) {
  if (!file) return;

  this.selectedFile = file;
  this.previewUrl = null;
  this.pdfPreview = null;
  this.error = null;

  if (file.type.startsWith("image/")) {
    this.previewUrl = URL.createObjectURL(file);
  } else if (file.type === "application/pdf") {
    this.pdfPreview = URL.createObjectURL(file);
  } else {
    this.error = "รองรับเฉพาะไฟล์รูปภาพ (JPG, PNG) และ PDF เท่านั้น";
    this.selectedFile = null;
  }
}

,
    removeFile() {
      this.selectedFile = null;
      this.previewUrl = null;
      this.pdfPreview = null;
      this.error = null;
      this.result = null;
      this.rawOcrText = null;
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
      }
    },
    async submitFile() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      console.log(this.selectedFile.name);
      formData.append("file", this.selectedFile);

      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        // console.log(response.data);
        this.rawOcrText = response.data.raw_text || "";
        const originalResult = response.data
        let fiileName = this.selectedFile.name.replace('.pdf', '.jpg');

        this.result = {
          store_name: originalResult.store_name || "",
          date_time: originalResult.date_time || "",
          receipt_number: originalResult.receipt_number || "",
          items: originalResult.items || [],
          vat: originalResult.vat
            ? parseFloat(originalResult.vat.replace(/[^0-9.-]+/g, ""))
            : 0,
          total: originalResult.total
            ? parseFloat(originalResult.total.replace(/[^0-9.-]+/g, ""))
            : 0,
          image_receipt: fiileName|| "",
        };

        if (this.autoSaveSwitch) {
          axios
            .post("http://localhost:5000/api/history_new", this.result)
            .then((response) => {
              this.showAlert(`Successfully recorded receipt information! Receipt Number: ${this.result.receipt_number}`, "success", 'bi bi-patch-check-fill me-1');
              delete this.result.image_receipt;
            })
            .catch((error) => {
              console.error(error);
            });
        }
      } catch (err) {
        this.error = "เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    formatPrice(price) {
      if (!price) return "฿0.00";
      return new Intl.NumberFormat("th-TH", {
        style: "currency",
        currency: "THB",
      }).format(price);
    },
    formatJSON(data) {
      return JSON.stringify(data, null, 2);
    },
    // async copyRawText() {
    //   if (this.rawOcrText) {
    //     await navigator.clipboard.writeText(this.rawOcrText);
    //     alert("คัดลอกข้อความแล้ว");
    //   }
    // },
    async copyJSON() {
      if (this.result) {
        await navigator.clipboard.writeText(
          this.formatJSON(this.result, null, 2)
        );
        // alert("คัดลอก JSON แล้ว");
        this.showAlert("คัดลอก JSON แล้ว", "success", 'bi bi-clipboard2-check-fill me-1');
      }
    },
    downloadJson() {
      this.isDownloading = true;
      this.downloadComplete = false;
      this.progress = 0;

      // อัปเดต Progress Bar
      let interval = setInterval(() => {
        if (this.progress < 100) {
          this.progress += 10; // เพิ่มขึ้นเรื่อยๆ จนถึง 90%
        }
      }, 200);

      setTimeout(() => {
        // สร้าง JSON และดาวน์โหลด
        const jsonString = this.formatJSON(this.result, null, 2);
        const blob = new Blob([jsonString], { type: "application/json" });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `receipt-${this.result.receipt_number}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        clearInterval(interval);
        this.progress = 100;

        setTimeout(() => {
          this.isDownloading = false;
          this.downloadComplete = true; // แสดงข้อความ Download สำเร็จ

          // ซ่อนข้อความหลัง 2 วินาที
          setTimeout(() => {
            this.downloadComplete = false;
          }, 1000);
        }, 1000);
      }, 2000); // สมมติว่าการดาวน์โหลดใช้เวลา 2 วินาที
    },
    toggleEditMode() {
      if (this.isEditing) {
        // บันทึกการแก้ไข
        try {
          // const parsedJson = JSON.parse(this.result);
          // ตรวจสอบโครงสร้างพื้นฐาน
          let parsedJson;
          if (typeof this.JsonEdit === "string") {
            parsedJson = JSON.parse(this.JsonEdit);
          } else if (typeof this.JsonEdit === "object") {
            parsedJson = this.JsonEdit; // ใช้ได้เลย ไม่ต้อง parse
          } else {
            throw new Error("Invalid data format");
          }

          let total_item_price = 0;
          parsedJson.items.forEach((item) => {
            total_item_price += item.price * item.quantity;
            // console.log(total_item_price);
          });

          parsedJson.total = total_item_price + parsedJson.vat;

          if (this.validateJsonStructure(parsedJson)) {
            // this.result = parsedJson;
            // console.log("This is edited :",this.result)
            this.isEditing = false;
            axios
              .put(
                `http://localhost:5000/api/history/${this.result.receipt_number}`,
                parsedJson
              )
              .then((response) => {
                // console.log(response.data);
                this.result = parsedJson;
                this.showAlert(`Edit Success! Receipt Number: ${parsedJson.receipt_number}`, "success",'bi bi-patch-check-fill me-1');
              })
              .catch((error) => {
                console.error(error);
              });
          } else {
            // alert("รูปแบบ JSON ไม่ถูกต้อง");
            this.showAlert("รูปแบบ JSON ไม่ถูกต้อง", "danger", 'bi bi-emoji-dizzy-fill');
          }
        } catch (error) {
          // alert("รูปแบบ JSON ไม่ถูกต้อง");
          this.showAlert("รูปแบบ JSON ไม่ถูกต้อง", "danger", 'bi bi-emoji-dizzy-fill');
        }
      } else {
        // เปิดโหมดแก้ไข
        this.JsonEdit = this.result;
        this.isEditing = true;
      }
    },
    validateJsonStructure(json) {
      // ตรวจสอบโครงสร้าง JSON พื้นฐาน
      return (
        json &&
        json.store_name &&
        json.date_time &&
        json.receipt_number &&
        Array.isArray(json.items) &&
        json.vat !== undefined &&
        json.total !== undefined
      );
    },
    addItem() {
      if (this.isEditing) {
        this.JsonEdit.items.push({ name: "", quantity: 1, price: 0.0 });
      }
    },
    removeItem(index) {
      if (this.isEditing) {
        this.JsonEdit.items.splice(index, 1);
      }
    },
    showAlert(message, type, icon) {
      this.alertMessage = message;
      this.alertClass = `alert-${type} py-2`;
      this.iconAlert = icon;
      setTimeout(() => {
        this.alertMessage = "";
        this.alertClass = "";
        this.iconAlert = '';
      }, 3000); // ซ่อน Alert หลังจาก 3 วินาที
    },
  },
//   mounted() {
//   this.data_test();
// }

};
</script>

<style scoped>
.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
  cursor: pointer;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #555555;
  background-color: #e8e8e8;
}

.upload-area.dragging {
  border-color: #555555;
  background-color: #e8e8e8;
}

.preview-in-upload {
  position: relative;
  width: 100%;
  padding: 1rem;
}

.preview-in-upload img ,.preview-in-upload iframe  {
  width: 100%;
  height: auto;
  height: 500px;
  object-fit: contain;
}

.preview-controls {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  background: rgba(0, 0, 0, 0.5);
  padding: 1rem;
  border-radius: 8px;
}

.preview-in-upload:hover .preview-controls {
  opacity: 1;
}

.raw-text-result,
.json-result {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  white-space: pre-wrap;
  font-size: 0.9rem;
  max-height: 400px;
  overflow-y: auto;
}

.json-edit-area {
  font-family: monospace;
  font-size: 0.9rem;
  background-color: white;
  height: 400px;
}

.table-responsive {
  margin-bottom: 1rem;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-dark {
  transition: all 0.2s ease;
}

.btn-dark:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.alert {
  margin-bottom: 1.5rem;
}

.spinner-border {
  width: 1.2rem;
  height: 1.2rem;
}

.progress_download {
  bottom: 20px; 
  right: 20px; 
  width: 350px; 
  height: 130px; 
  z-index: 2000;
}
</style>

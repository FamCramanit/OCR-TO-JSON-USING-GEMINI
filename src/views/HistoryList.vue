<template>
  <div class="container mt-2">
    <div
      v-if="alertCond == 'center'"
      :class="['alert', alertClass]"
      role="alert"
    >
    <i :class="['icon', iconAlert]"></i> {{ alertMessage }}
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="card border-0 rounded">
          <div
            class="card-header bg-dark text-white d-flex justify-content-between align-items-center"
          >
            <h5 class="mb-0">Receipt Extract History</h5>
            <div>
              <button class="btn btn-light btn-sm me-1" @click="clearFilters">
                <i class="bi bi-eraser me-1"></i>Clear
              </button>
              <button class="btn btn-primary btn-sm" @click="refreshHistory">
                <i class="bi bi-arrow-clockwise me-1"></i>Refresh
              </button>
            </div>
          </div>

          <div class="card-body rounded" style="background-color: #f9f9f9">
            <!-- Search and Filter Section -->
            <div class="row">
              <div class="col-md-4">
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-search"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control fw-medium"
                    v-model="searchQuery"
                    placeholder="Search by Store Name/Receipt Number"
                  />
                </div>
              </div>
              <div class="col-md-4">
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-calendar-range"></i>
                  </span>
                  <input
                    type="date"
                    class="form-control fw-medium"
                    v-model="dateFilter"
                  />
                </div>
              </div>
              <div class="col-md-4">
                <select class="form-select fw-medium" v-model="sortBy">
                  <option value="Newest">Latest - Oldest</option>
                  <option value="Oldest">Oldest - Latest</option>
                  <option value="Highest">Highest - Lowest</option>
                  <option value="Lowest">Lowest - Highest</option>
                </select>
              </div>
            </div>
            <div class="text-center">
              <p class="my-2 fw-medium">
                - Sort By : <span class="text-primary">{{ sortBy }}</span> -
              </p>
            </div>
            <div class="p-1">
              <!-- Header -->
              <div
                class="row bg-dark text-white py-3 rounded mb-2 mx-2 align-items-center fw-medium pe-1"
              >
                <div class="col text-center">Extract Date</div>
                <div class="col-5">S/Name</div>
                <div class="col text-center">Q/Item</div>
                <div class="col text-end">T/Price</div>
                <div class="col text-center d-flex justify-content-center align-items-center"> 
                  <div v-if="mode_action">
                                          <span 
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Select All"
                                        data-bs-content="Disabled popover"
                                      >
                                      <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
                                      </span>
                                    </div>
                  <p class="mb-0 me-1">Actions</p>
                  <div class="dropdown text-center">
                                <a
                                  type="button"
                                  class="link-light text-decoration-none dropdown show"
                                  id="dropdownUser2"
                                  data-bs-toggle="dropdown"
                                  aria-expanded="true"
                                >
                                  <i class="bi bi-three-dots-vertical"></i>
                                </a>
                                <div
                                  class="dropdown-menu p-1"
                                  aria-labelledby="dropdownUser2"
                                  data-popper-placement="top-start"
                                >
                                  <ul
                                    class="d-flex m-0 p-0 justify-content-center"
                                    style="list-style: none"
                                  >

                              
                                  <li>
                                      <span
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Change mode."
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-secondary btn-sm" @click="change_modeSelection">
                                          <i class="bi bi-arrow-repeat"></i>
                                        </button>
                                      </span>
                                    </li>

                                  <li>
                                      <span
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Download JSON."
                                        data-bs-content="Disabled popover"
                                      >
                                      <button
  class="btn btn-success btn-sm"
  @click="downloadJson(selectedReceipts)"
  :disabled="!Array.isArray(selectedReceipts) || selectedReceipts.length === 0"
>
  <i class="bi bi-download"></i>
</button>

                                      </span>
                                    </li>
                                    <li>
                                      <span
                                        class="d-inline-block"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Delete history."
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-danger btn-sm" @click="deleteHistory(selectedReceipts)" :disabled="!Array.isArray(selectedReceipts) || selectedReceipts.length === 0">
                                          <i class="bi bi-trash"></i>
                                        </button>
                                      </span>
                                    </li>
                                        
                                  </ul>
                                </div>
                              </div>
                </div>
                


                <!-- <div class="col text-center" v-if="mode_action">
      <input type="checkbox" v-model="selectAll" @change="toggleSelectAll"> 
    </div> -->
              </div>

              <!-- Schedule Items -->
              <div style="height: 450px">
                <div class="card_style p-2">
                  <template v-if="loading">
                    <div
                      class="d-flex justify-content-center align-items-center"
                      style="height: 350px"
                    >
                      <div class="text-center">
                        <div class="spinner-border text-primary"></div>
                        <p class="mt-2 mb-0">กำลังโหลดข้อมูล...</p>
                      </div>
                    </div>
                  </template>
                  <!-- Item 1 -->
                  <div v-else-if="filteredHistory.length">
                    <div
                      v-for="(receipt, index) in filteredHistory"
                      :key="index"
                    >
                      <div class="card border-0 shadow-sm mb-3 card_hover">
                        <div class="card-body">
                          <div class="row align-items-center">
                            <div class="col">
                              <!-- <h3 class="mb-0">16</h3> -->
                              <span class="text-muted fw-medium">{{
                                receipt.created_at
                              }}</span>
                            </div>
                            <div class="col-5">
                              <div class="d-flex align-items-center">
                                <div
                                  class="rounded-circle d-flex align-items-center justify-content-center me-3 fs-5 bg-light py-1 px-2"
                                >
                                  <i class="bi bi-receipt"></i>
                                </div>
                                <div>
                                  <div class="fw-medium">
                                    {{ receipt.store_name }}
                                  </div>
                                  <small
                                    style="font-size: 12px"
                                    class="text-muted bg-light p-1 rounded"
                                    >Receipt/N :
                                    {{ receipt.receipt_number }}</small
                                  >
                                </div>
                              </div>
                            </div>
                            <div class="col text-center fw-medium">
                              <small
                                :class="{
                                  'text-danger': receipt.items.length === 0,
                                  'text-muted': receipt.items.length !== 0,
                                }"
                                >{{ receipt.items.length }}</small
                              >
                            </div>
                            <div class="col text-end">
                              <span
                                class="badge bg-light text-dark"
                                style="font-size: 15px"
                                >{{ formatPrice(receipt.total) }}</span
                              >
                            </div>
                            <div class="col" v-if="!mode_action">
                              <div class="dropdown text-center">
                                <a
                                  type="button"
                                  class="link-dark text-decoration-none dropdown show"
                                  id="dropdownUser2"
                                  data-bs-toggle="dropdown"
                                  aria-expanded="true"
                                >
                                  <i class="bi bi-three-dots-vertical"></i>
                                </a>
                                <div
                                  class="dropdown-menu p-1"
                                  aria-labelledby="dropdownUser2"
                                  data-popper-placement="top-start"
                                >
                                  <ul
                                    class="d-flex m-0 p-0"
                                    style="list-style: none"
                                  >
                                    <li>
                                      <span
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="More detail."
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-primary btn-sm"
                                          type="button"
                                          data-bs-toggle="modal"
                                          data-bs-target="#OpenReceiptHistory"
                                          @click="viewReceipt(receipt)"
                                        >
                                          <i class="bi bi-eye"></i>
                                        </button>
                                      </span>
                                    </li>
                                    <li>
                                      <span
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Copy JSON"
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-secondary btn-sm"
                                          @click="copyJSON(receipt, 1)"
                                        >
                                          <i class="bi bi-clipboard-check"></i>
                                        </button>
                                      </span>
                                    </li>
                                    <li>
                                      <span
                                        class="d-inline-block me-2"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Download JSON."
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-success btn-sm"
                                          @click="downloadJson(receipt)"
                                        >
                                          <i class="bi bi-download"></i>
                                        </button>
                                      </span>
                                    </li>
                                    <li>
                                      <span
                                        class="d-inline-block"
                                        tabindex="0"
                                        data-bs-toggle="popover"
                                        data-bs-trigger="hover focus"
                                        title="Delete history."
                                        data-bs-content="Disabled popover"
                                      >
                                        <button
                                          class="btn btn-danger btn-sm"
                                          @click="
                                            deleteHistory(receipt)"
                                        >
                                          <i class="bi bi-trash"></i>
                                        </button>
                                      </span>
                                    </li>
                                  </ul>
                                </div>
                              </div>

                              <!-- <div class="d-flex justify-content-center">
                            <span class="d-inline-block me-2" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" title="More detail." data-bs-content="Disabled popover">
                              <button 
                            class="btn btn-primary btn-sm" type="button" data-bs-toggle="modal" data-bs-target="#OpenReceiptHistory" 
                            @click="viewReceipt(receipt)"
                          >
                            <i class="bi bi-eye"></i>
                          </button>
                            </span>

                            <span class="d-inline-block me-2" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" title="Edit selected." data-bs-content="Disabled popover">
                              <button 
                            class="btn btn-warning btn-sm"
                            @click="openEditModal(receipt)" data-bs-toggle="modal" data-bs-target="#editReceiptModal"
                          >
                            <i class="bi bi-pencil-square"></i>
                          </button>
                            </span>

                            <span class="d-inline-block me-2" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" title="Download JSON." data-bs-content="Disabled popover">
                              <button 
                            class="btn btn-success btn-sm"
                            @click="downloadJson(receipt)"
                          >
                            <i class="bi bi-download"></i>
                          </button>
                            </span>

                            <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" title="Delete history." data-bs-content="Disabled popover">
                              <button 
                            class="btn btn-danger btn-sm"
                            @click="deleteHistory(receipt.receipt_number)"
                          >
                            <i class="bi bi-trash"></i>
                          </button>
                            </span> 
                          </div> -->
                            </div>
                            <div class="col text-center"  v-if="mode_action">
                  <input type="checkbox" v-model="selectedReceipts" :value="receipt">
                </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <div
                      class="d-flex justify-content-center align-items-center"
                      style="height: 350px"
                    >
                      <div class="text-muted text-center">
                        <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                        No history of receipt extraction found.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>


            <div
              class="modal fade"
              id="OpenReceiptHistory"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-xl">
                <div class="modal-content">
                  <div class="modal-header bg-dark text-white">
                    <h4 class="modal-title">
                      <i class="bi bi-receipt"></i> Receipt details
                    </h4>
                    <button
                      type="button"
                      class="btn-close btn-close-white"
                      data-bs-dismiss="modal"
                    ></button>
                  </div>

                  <div class="modal-body" v-if="selectedReceipt">
                    <div
                      v-if="alertCond == 'modalDetail'"
                      :class="['alert', alertClass]"
                      role="alert"
                    >
                    <i :class="['icon', iconAlert]"></i> {{ alertMessage }}
                    </div>

                    <!-- ข้อมูลร้านค้า -->
                    <div class="row p-2 py-0">
                      <div class="col-md-5 p-2 border-end text-center">
                        <div 
    class="image-container"
    @click="zoomIn"
    @contextmenu.prevent="zoomOut"
    @mousedown="startPan"
    @mousemove="pan"
    @mouseup="endPan"
    @mouseleave="endPan"
    ref="container"
  >
    <img
      :src="require(`@/assets/uploads/${selectedReceipt.image_receipt}`)"
      class="zoom-image"
      :class="{ 'zoomed': isZoomed }"
      :style="zoomStyle"
      alt="Receipt"
      @dragstart.prevent
    />
  </div>
                      </div>

                      <div class="col-md-7 d-flex flex-column">
                        <div class="p-3 pt-0">
                          <div class="d-flex justify-content-between align-items-center">
                            <h4 class="mb-0">Store Information</h4>
                            <div>
                        <span
                          class="d-inline-block me-2"
                          tabindex="0"
                          data-bs-toggle="popover"
                          data-bs-trigger="hover focus"
                          title="Edit selected."
                          data-bs-content="Disabled popover"
                        >
                          <button
                            class="btn btn-warning btn-sm"
                            @click="toggleEdit"
                          >
                            <i
                              class="bi"
                              :class="isEditable ? 'bi-save' : 'bi-pencil'"
                            ></i>
                          </button>
                        </span>

                        <span
                          v-if="isEditable"
                          class="d-inline-block me-2"
                          tabindex="0"
                          data-bs-toggle="popover"
                          data-bs-trigger="hover focus"
                          title="Cancle edit."
                          data-bs-content="Disabled popover"
                        >
                          <button
                            class="btn btn-danger btn-sm"
                            @click="cancle_edit"
                          >
                            <i class="bi bi-x-lg"></i>
                          </button>
                        </span>

                        <span
                          class="d-inline-block me-2"
                          tabindex="0"
                          data-bs-toggle="popover"
                          data-bs-trigger="hover focus"
                          title="Copy JSON"
                          data-bs-content="Disabled popover"
                        >
                          <button
                            class="btn btn-secondary btn-sm"
                            @click="copyJSON(selectedReceipt, 2)"
                          >
                            <i class="bi bi-clipboard-check"></i>
                          </button>
                        </span>
                        <span
                          class="d-inline-block"
                          tabindex="0"
                          data-bs-toggle="popover"
                          data-bs-trigger="hover focus"
                          title="Downlaod JSON"
                          data-bs-content="Disabled popover"
                        >
                          <button
                            class="btn btn-success btn-sm"
                            @click="downloadJson(selectedReceipt)"
                          >
                            <i class="bi bi-download"></i>
                          </button>
                        </span>
                      </div>
                          </div>
                          <hr class="my-2" />
                          <p class="mb-1 fs-6 fw-medium">
                            Store Name:
                            <input
                              type="text"
                              :class="`form-control form-control-sm fs-6 ${
                                !isEditable ? 'bg-light border-0' : ''
                              }`"
                              v-model="selectedReceipt.store_name"
                              :disabled="!isEditable"
                            />
                          </p>
                          <p class="mb-1 fs-6 fw-medium">
                            Receipt Number:
                            <input
                              type="text"
                              :class="`form-control form-control-sm fs-6 ${
                                !isEditable ? 'bg-light border-0' : ''
                              }`"
                              v-model="selectedReceipt.receipt_number"
                              disabled
                            />
                          </p>
                          <p class="mb-0 fs-6 fw-medium">
                            Date:
                            <input
                              type="date"
                              :class="`form-control form-control-sm fs-6 ${
                                !isEditable ? 'bg-light border-0' : ''
                              }`"
                              v-model="selectedReceipt.date_time"
                              :disabled="!isEditable"
                            />
                          </p>
                        </div>

                        <div class="p-3 pt-0">
                          <h4 class="mb-0">Total Summary</h4>

                          <hr class="my-2" />
                          <p class="mb-1 fs-6 fw-medium" style="width: 50%">
                            VAT:
                            <input
                              type="number"
                              :class="`form-control form-control-sm fs-6 ${
                                !isEditable ? 'bg-light border-0' : ''
                              }`"
                              v-model.number="selectedReceipt.vat"
                              :disabled="!isEditable"
                            />
                          </p>
                          <p class="mb-0 fs-6 fw-medium" style="width: 50%">
                            Total Price:
                            <input
                              type="number"
                              :class="`form-control form-control-sm fs-6 ${
                                !isEditable ? 'bg-light border-0' : ''
                              }`"
                              v-model.number="selectedReceipt.total"
                              disabled
                            />
                          </p>
                        </div>
                        <div class="text-end mt-auto">
                          <p
                            class="mb-0 text-secondary"
                            style="font-size: 13px"
                          >
                            ( Extract Date: {{ selectedReceipt.created_at }} )
                          </p>
                        </div>
                      </div>
                    </div>

                    <hr class="mt-0 mb-2" />
                    <!-- ตารางรายการสินค้า -->
                    <div
                      class="d-flex justify-content-between align-items-center mx-2"
                    >
                      <h4 class="mb-0">
                        <i class="bi bi-list-nested"></i> List Item
                      </h4>

                      
                    </div>

                    <div
                      class="table-responsive p-2 pt-1 mt-1 overflow-y-auto"
                      style="max-height: 450px"
                    >
                      <table class="table">
                        <thead class="table-dark">
                          <tr>
                            <th class="text-center">#</th>
                            <th>Item</th>
                            <th class="text-center">Quantity</th>
                            <th class="text-end">Unit price</th>
                            <th class="text-end">Amount</th>
                            <th class="text-center" v-if="isEditable">
                              Delete
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(item, index) in selectedReceipt.items"
                            :key="index"
                          >
                            <td class="text-center">{{ index + 1 }}</td>
                            <td style="width: 500px;">
                              <input
                                type="text"
                                :class="`form-control form-control-sm ${
                                  !isEditable ? 'bg-light border-0' : ''
                                }`"
                                v-model="item.item_name"
                                :disabled="!isEditable"
                              />
                            </td>
                            <td class="text-center">
                              <input
                                type="number"
                                :class="`form-control form-control-sm text-center ${
                                  !isEditable ? 'bg-light border-0' : ''
                                }`"
                                v-model.number="item.quantity"
                                :disabled="!isEditable"
                              />
                            </td>
                            <td class="text-end">
                              <input
                                type="number"
                                :class="`form-control form-control-sm text-end ${
                                  !isEditable ? 'bg-light border-0' : ''
                                }`"
                                v-model.number="item.price"
                                :disabled="!isEditable"
                              />
                            </td>
                            <td class="text-end">
                              {{
                                formatPrice(item.price * (item.quantity || 1))
                              }}
                            </td>
                            <td class="text-center" v-if="isEditable">
                              <button
                                class="btn btn-danger btn-sm"
                                @click="removeItem(index)"
                                :disabled="!isEditable"
                              >
                                <i class="bi bi-trash"></i>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <div v-if="isEditable" class="text-center">
                        <button
                          class="btn btn-primary btn-sm"
                          @click="addItem"
                          :disabled="!isEditable"
                        >
                          <i class="bi bi-plus-circle me-1"></i>Add Item
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
    <p v-if="downloadComplete" class="text-success text-center mt-3 fw-medium" style="width: 100%;"><i class="bi bi-patch-check-fill me-2"></i>Download {{ quantity_item }} file Success!</p>
</div>
   

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReceiptHistory",
  data() {
    return {
      history: [],
      loading: false,
      searchQuery: "",
      dateFilter: "",
      sortBy: "Newest",
      selectedReceipt: null,
      showModal: false,
      editableReceipt: null,
      alertMessage: "", // ข้อความแจ้งเตือน
      alertClass: "", // คลาสของ Alert (success, danger, warning, etc.)
      alertCond: "", // เงื่อนไขแสดง Alert (true, false)
      iconAlert : "",
      isEditable: false,
      isZoomed: false,
      isPanning: false,
      startX: 0,
      startY: 0,
      translateX: 0,
      translateY: 0,
      zoomStyle: {
        transform: "scale(1)",
        transformOrigin: "center",
        translate: "0px 0px"
      },
      isDownloading: false,
      progress: 0,
      downloadComplete: false,
      quantity_item: 0,
      selectedReceipts: [], // รายการที่ถูกเลือก
      selectAll: false, // สถานะปุ่มเลือกทั้งหมด
      mode_action: false,
    };
  },
  computed: {
    filteredHistory() {
      let filtered = [...this.history];

      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (receipt) =>
            receipt.store_name.toLowerCase().includes(query) ||
            receipt.receipt_number.toLowerCase().includes(query)
        );
      }

      // Date filter
      if (this.dateFilter) {
        const filterDate = new Date(this.dateFilter).setHours(0, 0, 0, 0);
        filtered = filtered.filter((receipt) => {
          const receiptDate = new Date(receipt.created_at).setHours(0, 0, 0, 0);
          return receiptDate === filterDate;
        });
      }

      // Sort
      switch (this.sortBy) {
        case "Newest":
          filtered.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          break;
        case "Highest": // เรียงจากราคาสูง -> ต่ำ
          filtered.sort(
            (a, b) =>
              parseFloat(String(b.total).replace(/[^0-9.]/g, "")) -
              parseFloat(String(a.total).replace(/[^0-9.]/g, ""))
          );
          break;
        case "Lowest": // เรียงจากราคาต่ำ -> สูง
          filtered.sort(
            (a, b) =>
              parseFloat(String(a.total).replace(/[^0-9.]/g, "")) -
              parseFloat(String(b.total).replace(/[^0-9.]/g, ""))
          );
          break;
        default: // newest
          filtered.sort(
            (a, b) => new Date(a.created_at) - new Date(b.created_at)
          );
      }

      return filtered;
    },
  },
  methods: {
    async fetchHistory() {
      this.loading = true;

      try {
        const response = await axios.get("http://127.0.0.1:5000/api/history");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        this.history = response.data;
        console.log(this.history);
      } catch (error) {
        console.error("Failed to fetch history:", error);
        // Handle error appropriately
      } finally {
        this.loading = false;
      }
    },
    showAlert(message, type, cond, icon) {
      this.alertMessage = message;
      this.alertClass = `alert-${type} py-2`;
      this.alertCond = cond;
      this.iconAlert = icon;
      setTimeout(() => {
        this.alertMessage = "";
        this.alertClass = "";
        this.alertCond = "";
        this.iconAlert = "";
      }, 3000); // ซ่อน Alert หลังจาก 3 วินาที
    },
    clearFilters() {
      this.searchQuery = "";
      this.dateFilter = "";
      this.sortBy = "Newest";
      this.selectAll= false; // สถานะปุ่มเลือกทั้งหมด
      this.mode_action= false;
      this.selectedReceipts=[];
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("th-TH", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    formatPrice(price) {
      if (!price) return "0.00";
      return new Intl.NumberFormat("th-TH", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(price);
    },
    addItem() {
      if (this.isEditable) {
        this.selectedReceipt.items.push({ name: "", quantity: 1, price: 0.0 });
      }
    },
    removeItem(index) {
      if (this.isEditable) {
        this.selectedReceipt.items.splice(index, 1);
      }
    },
    toggleEdit() {
      if (this.isEditable) {
        // เมื่อบันทึก ทำอะไรกับข้อมูล เช่น บันทึกลง DB หรือแจ้งเตือน
        try {
          let parsedJson;

          // ตรวจสอบว่าเป็น String หรือ Object
          if (typeof this.selectedReceipt === "string") {
            parsedJson = JSON.parse(this.selectedReceipt);
          } else if (typeof this.selectedReceipt === "object") {
            parsedJson = this.selectedReceipt; // ใช้ได้เลย ไม่ต้อง parse
          } else {
            throw new Error("Invalid data format");
          }

          // console.log(parsedJson);
          let total_item_price = 0;
          parsedJson.items.forEach((item) => {
            total_item_price += item.price * item.quantity;
            console.log(total_item_price);
          });

          parsedJson.total = total_item_price + parsedJson.vat;

          axios
            .put(
              `http://localhost:5000/api/history/${parsedJson.receipt_number}`,
              parsedJson
            )
            .then((response) => {
              this.refreshHistory();
              // alert(response.data.message);
              this.showAlert(response.data.message, "success", "modalDetail", 'bi bi-patch-check-fill me-1');
            })
            .catch((error) => {
              // console.error(error);
              this.showAlert(error, "danger", "modalDetail", 'bi bi-emoji-dizzy-fill');
            });
        } catch (error) {
          // alert('รูปแบบ JSON ไม่ถูกต้อง: ' + error.message);
          this.showAlert(
            "รูปแบบ JSON ไม่ถูกต้อง: " + error.message,
            "danger",
            "modalDetail",
            'bi bi-emoji-dizzy-fill'
          );
        }
      }
      this.isEditable = !this.isEditable; // สลับสถานะแก้ไข
    },
    cancle_edit() {
      this.isEditable = !this.isEditable;
    },
    async copyJSON(jsonData, x) {
      if (jsonData) {
        await navigator.clipboard.writeText(
          JSON.stringify(this.filterJsonFormat(jsonData), null, 2)
        );
        // alert('คัดลอก JSON แล้ว');
        if (x == 1) {
          this.showAlert("คัดลอก JSON แล้ว", "success", "center", 'bi bi-clipboard2-check-fill me-1');
        } else {
          this.showAlert("คัดลอก JSON แล้ว", "success", "modalDetail", 'bi bi-clipboard2-check-fill me-1');
        }
      }
    },
    viewReceipt(receipt) {
      this.selectedReceipt = receipt;
      // this.showModal = true;
    },
    filterJsonFormat(data) {
      const filteredData = {
        store_name: data.store_name,
        date_time: data.date_time,
        receipt_number: data.receipt_number,
        items: data.items.map(({ item_name, price, quantity }) => ({
          item_name,
          price,
          quantity,
        })),
        total: data.total,
        vat: data.vat,
      };
      return filteredData;
    },
    downloadJson(receipt) {
  if (!receipt) {
    console.error("Invalid receipt data:", receipt);
    return;
  }

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
    try {
      // ตรวจสอบว่า receipt เป็น Array หรือไม่
      const dataArray = Array.isArray(receipt) ? receipt : [receipt];

      // วนลูปสร้างไฟล์แยกสำหรับแต่ละใบเสร็จ
      dataArray.forEach((item) => {
        this.quantity_item += 1;
        const filteredData = this.filterJsonFormat(item);
        const jsonString = JSON.stringify(filteredData, null, 2);
        const blob = new Blob([jsonString], { type: "application/json" });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;

        // ตั้งชื่อไฟล์ตาม receipt_number หรือใช้ค่า default
        const fileName = item.receipt_number
          ? `receipt-${item.receipt_number}.json`
          : "receipt.json";
        link.download = fileName;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      });

      clearInterval(interval);
      this.progress = 100;

      setTimeout(() => {
        this.isDownloading = false;
        this.downloadComplete = true; // แสดงข้อความ Download สำเร็จ

        // ซ่อนข้อความหลัง 2 วินาที
        setTimeout(() => {
          this.downloadComplete = false;
          this.quantity_item = 0;
        }, 1000);
      }, 1000);
    } catch (error) {
      console.error("Error generating JSON:", error);
      this.isDownloading = false;
    }
  }, 2000); // สมมติว่าการดาวน์โหลดใช้เวลา 2 วินาที
}
,
async deleteHistory(ids) {
  let select_delete = [];

  if(Array.isArray(ids)) {
    select_delete = ids
  } else {
    select_delete.push(ids)
  }
  if (!select_delete.length) {
    this.showAlert("No receipts selected for deletion!", "warning", "center", 'bi bi-slash-circle');
    return;
  }

  if (!confirm(`Are you sure you want to delete ${select_delete.length} receipts?`)) return;

  try {
    await Promise.all(
      select_delete.map((id) => axios.delete(`http://127.0.0.1:5000/api/history/${id.receipt_number}`))
    );

    await this.fetchHistory();
    this.showAlert(
      `Delete Success! ${ids.length} receipts deleted.`,
      "success",
      "center",
      'bi bi-patch-check-fill me-1'
    );
  } catch (error) {
    this.showAlert("Failed to delete some receipts.", "danger", "center", 'bi bi-emoji-dizzy-fill');
    console.error("Error deleting receipts:", error);
  }
}
,
    refreshHistory() {
      this.fetchHistory();
    },
    zoomIn(event) {
      if (!this.isPanning && !this.isZoomed) {
        this.isZoomed = true;
        const container = event.currentTarget;
        const { left, top, width, height } = container.getBoundingClientRect();
        const x = ((event.clientX - left) / width) * 100;
        const y = ((event.clientY - top) / height) * 100;

        this.translateX = 0;
        this.translateY = 0;
        
        this.zoomStyle = {
          transform: "scale(2.5)",
          transformOrigin: `${x}% ${y}%`,
          transition: "transform 0.3s ease-out",
          translate: "0px 0px"
        };
      }
    },

    zoomOut(event) {
      if (!this.isPanning && this.isZoomed) {
        this.isZoomed = false;
        this.resetZoom();
      }
    },

    startPan(event) {
      if (this.isZoomed && event.button === 0) { // Only start panning on left click
        this.isPanning = true;
        this.startX = event.clientX - this.translateX;
        this.startY = event.clientY - this.translateY;
      }
    },

    pan(event) {
      if (this.isPanning && this.isZoomed) {
        const container = this.$refs.container;
        const rect = container.getBoundingClientRect();
        
        // Calculate new position
        let newX = event.clientX - this.startX;
        let newY = event.clientY - this.startY;
        
        // Add boundaries for panning
        const maxPanX = rect.width * 0.5;
        const maxPanY = rect.height * 0.5;
        
        newX = Math.max(Math.min(newX, maxPanX), -maxPanX);
        newY = Math.max(Math.min(newY, maxPanY), -maxPanY);
        
        this.translateX = newX;
        this.translateY = newY;
        
        this.zoomStyle = {
          ...this.zoomStyle,
          transition: "none",
          translate: `${newX}px ${newY}px`
        };
      }
    },

    endPan() {
      this.isPanning = false;
    },

    resetZoom() {
      this.translateX = 0;
      this.translateY = 0;
      this.zoomStyle = {
        transform: "scale(1)",
        transformOrigin: "center",
        transition: "all 0.3s ease-out",
        translate: "0px 0px"
      };
    },
    toggleSelectAll() {
    if (this.selectAll) {
      this.selectedReceipts = this.filteredHistory.map(receipt => receipt);
      // console.log(this.selectedReceipts);
    } else {
      this.selectedReceipts = [];
      // console.log(this.selectedReceipts);
    }
  },
  change_modeSelection() {
    this.selectedReceipts = [];
    this.selectAll = false
    this.mode_action = !this.mode_action
  }


    // Remove the zoomImage and resetZoom methods as they're no longer needed

  },
  mounted() {
    this.fetchHistory();
  },
};
</script>

<style scoped>
.table td {
  vertical-align: middle;
}

.spinner-border {
  width: 1.5rem;
  height: 1.5rem;
}

.card_style {
  max-height: 450px;
  overflow-y: auto;
}

.card_hover {
  transition: 0.3s ease;
}

.card_hover:hover {
  
  background-color: rgb(246, 245, 245);
}



.image-container {
  position: relative;
  display: inline-block;
  overflow: hidden;
  max-width: 350px;
  height: auto;
  border: 2px dashed;
  border-radius: 10px;
  cursor: zoom-in;
}

.zoom-image {
  width: 100%;
  transition: transform 0.3s ease-out;
  user-select: none;
}

.zoom-image.zoomed {
  cursor: grab;
}

.zoom-image.zoomed:active {
  cursor: grabbing;
}

/* Add tooltip style */
.image-container::after {
  content: 'Right-click to zoom in, Left-click to zoom out';
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
  white-space: nowrap;
  pointer-events: none;
}

.image-container:hover::after {
  opacity: 1;
}

.progress_download {
  bottom: 20px; 
  right: 20px; 
  width: 350px; 
  height: 130px; 
  z-index: 2000;
}
</style>

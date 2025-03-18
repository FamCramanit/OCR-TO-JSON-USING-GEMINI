<template>
    <div v-if="isLoading" class="position-fixed w-100 h-100">
      <div class="loader d-flex justify-content-center align-items-center">
        <div class="text-center">
          <img src="@/assets/image/kingkong.gif" alt="loading..." />
          <p class="mb-0 text-secondary fw-medium">Loading...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AnimationPage',
    data() {
      return {
        isLoading: true, // ใช้ตัวแปรนี้ในการควบคุมการแสดงผล
      };
    },
    mounted() {
      // จำลองการโหลดข้อมูล
      setTimeout(() => {
        this.isLoading = false; // ปิดการแสดงแอนิเมชั่นเมื่อโหลดเสร็จ
      }, 3000); // แค่เป็นตัวอย่างการโหลด 3 วินาที
    },
  };
  </script>
  
  <style scoped>
  .loader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255); /* พื้นหลังโปร่งใส */
  }
  
  .loader img {
    width: 100px;
    animation: pulse 1.5s infinite;
  }
  
  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
  }
  </style>
  
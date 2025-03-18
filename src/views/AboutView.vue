<template>
  <div class="container mt-4">
    <h2 class="text-center mb-1">*************</h2>
    <p class="mb-2 text-secondary text-center">
      Members who helped develop this project.
    </p>
    <hr />
    <div class="d-flex justify-content-center">
      <div
        class="row row-cols-1 row-cols-md-4 g-1 align-items-center"
        style="height: 450px; width: 100%"
      >
        <div class="col" v-for="member in members" :key="member.id">
          <div class="card h-100 border-0">
            <div class="text-center mb-2">
              <img
                :src="member.avatar"
                class="card-img-top rounded-circle shadow"
                style="cursor: pointer"
                alt="Avatar"
              />
            </div>
            <div class="card-body p-2 text-center">
              <h5 class="card-title">{{ member.name }}</h5>
              <p class="card-text">
                <strong>Email: </strong>
                <span
                  ><a href="">{{ member.email }}</a></span
                >
                <br />
                <strong>Role: </strong>
                <span class="ms-2 fw-bold">{{ member.status }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PFam from "@/assets/creater/black.png";
import Meen from "@/assets/creater/black.png";
import Yod from "@/assets/creater/black.png";
import Dant from "@/assets/creater/black.png";

export default {
  name: "AboutView",
  data() {
    return {
      members: [
        {
          id: 1,
          name: "Yod chaaaaiiii",
          email: "Yod@example.com",
          status: "*******",
          avatar: Yod,
        },
        {
          id: 2,
          name: "Fam",
          email: "Fam@example.com",
          status: "*******",
          avatar: PFam,
        },
        {
          id: 3,
          name: "BangMeen",
          email: "Meen@example.com",
          status: "*******",
          avatar: Meen,
        },
        {
          id: 4,
          name: "I Dant!",
          email: "Dant@example.com",
          status: "*******",
          avatar: Dant,
        },
        // ข้อมูลสมาชิกอื่นๆ
      ],
    };
  },
  methods: {
    viewMember(id) {
      console.log(`ดูข้อมูลสมาชิก ${id}`);
    },
    editMember(id) {
      console.log(`แก้ไขข้อมูลสมาชิก ${id}`);
    },
    statusClass(status) {
      if (status === "สมาชิก") return "bg-success text-white";
      if (status === "ผู้ดูแล") return "bg-primary text-white";
      return "bg-secondary text-white";
    },
  },
};
</script>

<style scoped>
.card {
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-10px);
}

.card-img-top {
  height: 200px;
  width: 200px;
  object-fit: cover;
}

.card-text {
  font-size: 0.9rem;
}
</style>

<template>
  <div class="home">
    <main
      style="height: 600px"
      class="d-flex justify-content-center align-items-center"
    >
      <div class="text-center" style="width: 700px">
        <h2>Easily extract text from receipts.</h2>
        <p class="lead" style="font-size: 17px">
          Simply upload an image of the receipt, and the system will process it
          and display the data in JSON format or any other usable format
          instantly. No need to manually enter data from receipts anymore,
          reducing hassle and minimizing errors that may occur from typing
          mistakes. The extracted data can be directly used in accounting
          systems or other data management software.
        </p>
        <p class="lead">
          <router-link to="/Extract" class="btn btn-sm btn-secondary"
            >Extract Receipt Now!</router-link
          >
        </p>
      </div>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "HomeView",
  components: {},
};
</script>

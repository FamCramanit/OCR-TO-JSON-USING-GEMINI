<template>
  <div>
  <Animation style="z-index:1;" msg="Welcome to Your Vue.js App"/>
  <header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex align-items-center justify-content-between">
        <router-link to="/" class="d-flex align-items-end mb-lg-0 text-white text-decoration-none h3">
          OCR | <span style="font-size: 15px;" class="border-top pt-0 ms-1">Extract Receipt</span>
        </router-link>

        <ul class="nav col-12 col-lg-auto mb-2 justify-content-center mb-md-0" style="font-size: 15px;">
  <li>
    <router-link to="/" 
                 class="nav-link px-2 fw-medium" 
                 :class="{ 'text-secondary': $route.path === '/', 'text-white': $route.path !== '/' }">Home</router-link>
  </li>
  <li>
    <router-link to="/Extract" 
                 class="nav-link px-2 fw-medium" 
                 :class="{ 'text-secondary': $route.path === '/Extract', 'text-white': $route.path !== '/Extract' }">Extract</router-link>
  </li>
  <li>
    <router-link to="/History" 
                 class="nav-link px-2 fw-medium" 
                 :class="{ 'text-secondary': $route.path === '/History', 'text-white': $route.path !== '/History' }">History</router-link>
  </li>
  <li>
    <router-link to="/About" 
                 class="nav-link px-2 fw-medium" 
                 :class="{ 'text-secondary': $route.path === '/About', 'text-white': $route.path !== '/About' }">About Us</router-link>
  </li>

  
</ul>


<!--<form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
  div class="input-group">
  <input type="search" class="form-control form-control-dark" placeholder="Search..." aria-label="Search">
  <button type="submit" class="btn btn-primary"><i class="bi bi-search"></i></button>
</div>
</form>-->
<!--
<div class="text-end">
          <button type="button" class="btn btn-outline-light me-2">Login</button>
          <button type="button" class="btn btn-light">Sign-up</button>
          <div class="dropdown">
  <a class="btn btn-secondary dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Sub-function</a>

  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="#">Action</a></li>
    <li><a class="dropdown-item" href="#">Another action</a></li>
    <li><a class="dropdown-item" href="#">Something else here</a></li>
  </ul>
</div>
        </div>
-->
      </div>
    </div>
  </header>
  <div class="border-bottom border-1 text-secondary container mt-1 fw-medium" style="width: 100%; font-size: 13px;">{{ $route.path === '/' ? "/Home" : $route.path }}</div>
  <router-view/>
  <div class="container">
    <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
      <div class="col-md-4 d-flex align-items-center">
        <router-link to="/" class="d-flex align-items-end mb-lg-0 text-white text-decoration-none h4 me-4 text-body-secondary">
          OCR | <span style="font-size: 15px;" class="border-top border-black pt-0 ms-1">Extract Receipt</span>
        </router-link>
        
        <span class="mb-md-0 text-body-secondary fw-medium">© 2025 Test, V3.0 Full</span>
      </div>

      <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
        <li class="ms-3">
          <a class="text-body-secondary" href="#">
            <i class="bi bi-twitter" style="font-size: 24px;"></i>
          </a>
        </li>
        <li class="ms-3">
          <a class="text-body-secondary" href="#">
            <i class="bi bi-instagram" style="font-size: 24px;"></i>
          </a>
        </li>
        <li class="ms-3">
          <a class="text-body-secondary" href="#">
            <i class="bi bi-facebook" style="font-size: 24px;"></i>
          </a>
        </li>
      </ul>
    </footer>
  </div>
  </div>
</template>

<script>
import Animation from '@/components/Animation.vue'
export default {
  name: 'App',
  components: {
    Animation
  }
}
</script>

<style scope>
/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px grey; 
  border-radius: 0px;
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 0px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}
</style>

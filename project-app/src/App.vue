<script setup>
import { ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

import assets from './assets/assets'

const router = useRouter();
const route = useRoute();
const store = useStore();
const loadedScripts = ref(false);
const isSidebarOpen = ref(false);

const isAuthenticated = ref(store.state.refresh !== null?true:false);
const usercat = ref(store.getters.usercat);
const currentPage = ref(store.getters.currentTab);

const isDark = ref(store.getters.isDark);
const isShowText = ref(true);

watch(() => store.state.refresh, (newVal) => {
  isAuthenticated.value = newVal !== null ? true : false;
}, { immediate: true });

watch(() => store.state.usercat, (newVal) => {
  usercat.value = newVal;
}, { immediate: true });

watch(() => store.state.currentPage, (newVal) => {
  currentPage.value = newVal;
}, { immediate: true });

watch(() => store.state.isDark, (newVal) => {
  isDark.value = newVal;
}, { immediate: true });





const initializeScroll = () => {
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
}

const logout = () => {
  const redirectPath = '/login'; 
  router.push(redirectPath);
}

const isSmallSize = () => {
  return window.innerWidth <= 786;
}


const toggleSideBar = () => {
  if(!isSidebarOpen.value){
    document.body.classList.add('g-sidenav-pinned');
  } else {
    document.body.classList.remove('g-sidenav-pinned');
  }
  isSidebarOpen.value =!isSidebarOpen.value;

}


const toggleDarkMode = (init=false) => {
  
  if(init){
    if(store.getters.isDark) {
      document.body.classList.add('dark-version');
      isDark.value=true;
    }
    else{
      document.body.classList.remove('dark-version');
      isDark.value=false;
    }
    return;
  }

  if(isDark.value) {
    document.body.classList.remove('dark-version');
    store.commit('setIsDark',false)
    isDark.value=false;
  }
  else{
    document.body.classList.add('dark-version');
    store.commit('setIsDark',true);
    isDark.value=true;
  }
}

const loadScripts = () => {
  const scripts = [
     "./assets/js/material-dashboard.js"
  ];

      
      if (!loadedScripts.value) {
              scripts.forEach(script => {
          const scriptElement = document.createElement('script');
          scriptElement.src = script;
          scriptElement.async = false; // Ensure scripts are executed in order
          document.body.appendChild(scriptElement);
              });
          loadedScripts.value = true;
          }               
}





onMounted(() => {
  
  //loadScripts();
  toggleDarkMode(true);
  initializeScroll();
});

</script>

<template>
  <aside v-if="isAuthenticated"  class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3   bg-gradient-dark" :class="{'bg-gradient-dark':isSidebarOpen, 'bg-transparent':!isSidebarOpen,'limited-width':!isShowText}" id="sidenav-main">
    <div class="d-flex" style="justify-content: flex-start; width:100%;padding:.5rem 1rem;"  @click="toggleSideBar" v-if="isSmallSize()">
      <i class="material-icons opacity-10" style="font-size:30px;" >chevron_left</i>
    </div>
    <!--
    <div class="d-flex " style="justify-content: flex-start; width:100%;padding:.5rem;cursor:pointer" @click="isShowText = !isShowText" :class="{'justify-content-center':!isShowText}" v-else>
      <i class="material-icons opacity-10" style="font-size:30px;" v-if="!isShowText">arrow_forward_ios</i>
      <i class="material-icons opacity-10" style="font-size:30px;" v-else>arrow_back_ios_new</i>
    </div>
    -->
    <hr class="horizontal light mt-0 mb-2">
    <div class="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/" class="nav-link text-white " :class="{'bg-gradient-primary':currentPage=='dashboard'}">
            <div class="text-white text-center me-2 d-flex align-items-center justify-content-center">
              <i class="material-icons opacity-10">dashboard</i>
            </div>
            <span class="nav-link-text ms-1" v-if="isShowText">Dashboard</span>
          </router-link>
        </li>
        
        <li class="nav-item" v-if="usercat=='maintenance_supervisor' || usercat == 'admin'">
          <router-link to="projects" class="nav-link text-white " :class="{'bg-gradient-primary':currentPage=='projects'}">
            <div class="text-white text-center me-2 d-flex align-items-center justify-content-center">
              <i class="material-icons opacity-10">engineering</i>
            </div>
            <span class="nav-link-text ms-1" v-if="isShowText">Projects</span>
          </router-link>
        </li>
       
        <li class="nav-item my-4" v-if="usercat=='maintenance_supervisor' || usercat == 'security_officer'">
          <router-link to="profile" class="nav-link text-white " :class="{'bg-gradient-primary':currentPage=='profile'}">
            <div class="text-white text-center me-2 d-flex align-items-center justify-content-center">
              <i class="material-icons opacity-10">person</i>
            </div>
            <span class="nav-link-text ms-1" v-if="isShowText">Profile</span>
          </router-link>
        </li>
      </ul>

      




      
    </div>
    <div class="sidenav-footer position-absolute w-100 bottom-0 ">
      <div class="mx-3">
        
        <span class="btn bg-gradient-primary w-100" @click="logout()" type="button"> 
          <i class="material-icons opacity-10">logout</i>
          <span class="mx-2" v-if="isShowText">Logout</span></span>
      </div>
    </div>
  </aside>

  <main class="main-content position-relative max-height-vh-100 h-100 border-radius-lg " >
    <nav v-if="isAuthenticated" class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl" id="navbarBlur" data-scroll="true">
      <div class="container-fluid py-1 px-3">
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb bg-transparent mb-0 pb-0 pt-1 px-0 me-sm-6 me-5">
            <li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="javascript:;">Pages</a></li>
            <li class="breadcrumb-item text-sm text-dark active" aria-current="page" style="text-transform: capitalize;">{{store.getters.currentPage.replace('-',' ')}}</li>
          </ol>
          <h6 class="font-weight-bolder mb-0" style="text-transform: capitalize;">{{store.getters.currentPage.replace('-',' ')}}</h6>
        </nav>
        <div class="collapse navbar-collapse mt-sm-0 mt-2 me-md-0 me-sm-4" id="navbar">
         
          <ul class="navbar-nav  justify-content-end">
           
            <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
              <a href="javascript:;" class="nav-link text-body p-0" @click="toggleSideBar">
                <div class="sidenav-toggler-inner">
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                  <i class="sidenav-toggler-line"></i>
                </div>
              </a>
            </li>
           
          </ul>
        </div>
      </div>
    </nav>


    <router-view></router-view>

  </main>

  <div class="fixed-plugin" v-if="isAuthenticated">
    <span v-if="!isDark" class="fixed-plugin-button text-dark position-fixed px-3 py-2" style="background:var(--bs-gray-dark);" @click="toggleDarkMode()">
      <i class="material-icons py-2" style="color:var(--bs-white);">dark_mode</i>
     
    </span>
    <span v-else class="fixed-plugin-button text-dark position-fixed px-3 py-2" style="background:var(--bs-white);" @click="toggleDarkMode()">
      <i class="material-icons py-2" style="color:var(--bs-dark);">light_mode</i>
     
    </span>
   
  </div>
</template>

<style lang="scss">  
@import url("./assets/css/nucleo-icons.css");
@import url("./assets/css/nucleo-svg.css");
@import url("./assets/css/material-dashboard.css");





aside.limited-width{
  width:5.5rem !important;
  transition: all .3s ease;
}

button:not(:disabled):hover, span.custombutton:hover{
  opacity:.8 !important;
}

</style>

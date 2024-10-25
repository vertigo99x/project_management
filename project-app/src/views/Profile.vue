

<script setup>
import { ref, reactive, inject, onMounted } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import moment from 'moment';
import axios from 'axios';


const $http = inject('$http');
const router = useRouter();
const route = useRoute(); // Use useRoute to get current route
const store = useStore();

const isLoading = ref(false);
const userData = ref(null);

const isChangePassword = ref(false);
const oldPassword = ref('');
const password = ref('');
const confirmPassword = ref('');


async function refreshToken(callback) {
    try {
        const response = await $http.post('api/token/refresh', {
            refresh: store.getters.refresh,
        });

        if (response.data.access) {
            store.commit('setAccess', response.data.access);
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            await callback();  // Call the callback function after token refresh
        } else {
            router.push('/login');  // Redirect to login if no access token is received
        }
    } catch (error) {
        console.error('Failed to refresh token', error);
        router.push('/login');  // Redirect to login on token refresh failure
    }
}






async function getUserData() {
    isLoading.value = true;
    try {
        const response = await $http.get('accounts/userdata');
        userData.value = response.data;
        store.commit('setUsercat', userData.value.role)
        //userCat.value = userData.role
        isLoading.value = false;
    } catch (error) {
    isLoading.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(getUserData);
            } else {
                // Handle other status codes
                console.error(`Error ${status}: ${error.response.data.message}`);
                toast.error(`Error ${status}: ${error.response.data.message}`, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
            }
        } else if (error.request) {
            // Request made but no response received
            console.error('No response received:', error.request);
            toast.error('No response received. Please try again later.', {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        } else {
            // Other errors
            console.error('Error', error);
            toast.error(`Error: ${error.message}`, {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        }
    }
}

async function changePassword(){
  isLoading.value = true;
  const data = {
    old_password: oldPassword.value,
    new_password: password.value,
  }
    try {
        const response = await $http.post('accounts/change-password/', data);
        
        toast.info(response.data.message, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
        isLoading.value = false;
        router.push('/login')

    } catch (error) {
    isLoading.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(changePassword);
            } else {
                // Handle other status codes
                console.error(`Error ${status}: ${error.response.data.message}`);
                toast.error(`Error ${status}: ${error.response.data.message}`, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
            }
        } else if (error.request) {
            // Request made but no response received
            console.error('No response received:', error.request);
            toast.error('No response received. Please try again later.', {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        } else {
            // Other errors
            console.error('Error', error);
            toast.error(`Error: ${error.message}`, {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        }
    }
}



const validatePassword = () => {
  if(password.value.length < 8){
    return false;
  }
  return true;
}


onMounted(() => {
  store.commit('setCurrentPage', 'profile')
    getUserData();
})


</script>

<template>
    <div class="container-fluid px-2 px-md-4" v-if="userData">
       
        <div class="page-header min-height-300 border-radius-xl mt-4" style="background-image: url('https://images.unsplash.com/photo-1531512073830-ba890ca4eba2?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');">
          <span class="mask  bg-gradient-secondary  opacity-6"></span>
        </div>
        <div class="card card-body mx-3 mx-md-4 mt-n6">
          <div class="row gx-4 mb-2">
            <div class="col-auto">
              <div class="avatar avatar-xl position-relative">
                <img :src="userData.profile_image_url" alt="profile_image" class="w-100 border-radius-lg shadow-sm">
              </div>
            </div>
            <div class="col-auto my-auto">
              <div class="h-100">
                <h5 class="mb-1">
                  {{ userData.last_name}}  {{ userData.first_name}}
                </h5>
                <p class="mb-0 font-weight-normal text-sm" style="text-transform: capitalize;">
                    {{ userData.role.replace('_', ' ')}}
                </p>
              </div>
            </div>
            
          </div>
          <div class="row">
            <div class="row">
              
              <div class="col-12 col-xl-4">
                <div class="card card-plain h-100">
                  <div class="card-header pb-0 p-3">
                    <div class="row">
                      <div class="col-md-8 d-flex align-items-center">
                        <h6 class="mb-0">Profile Information</h6>
                      </div>
                     
                    </div>
                  </div>
                  <div class="card-body p-3">
                   
                    <hr class="horizontal gray-light my-1">
                    <ul class="list-group">
                      <li class="list-group-item border-0 ps-0 pt-0 text-sm"><strong class="text-dark">Full Name:</strong> &nbsp;  {{ userData.last_name}}  {{ userData.first_name}}</li>
                      <li class="list-group-item border-0 ps-0 text-sm"><strong class="text-dark">Mobile:</strong> &nbsp; {{userData.phone_number}}</li>
                      <li class="list-group-item border-0 ps-0 text-sm"><strong class="text-dark">Email:</strong> &nbsp; {{ userData.email }}</li>
                      <li class="list-group-item border-0 ps-0 text-sm"><button @click="isChangePassword=true" v-if="!isChangePassword" class="bg-gradient-primary text-white shadow-primary" style="border:1px solid var(--bs-primary);padding:.5rem 1rem;border-radius: .5rem;margin-top:2rem;">Change Password</button></li>
                      
                    </ul>
                  </div>
                </div>
              </div>
             
              <div class="col-12 col-xl-4 fade" v-if="isChangePassword">
                <div class="close-button">
                  <span class="svg-icon"
                    ><svg
                      @click="isChangePassword=false;"
                      xmlns="http://www.w3.org/2000/svg"
                      height="48"
                      viewBox="0 -960 960 960"
                      width="48"
                    >
                      <path
                        d="m249-207-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"
                      /></svg
                  ></span>
                </div>
                <div class="field">
                    <input type="password" placeholder="Old Password" v-model="oldPassword" :class="{'redify':oldPassword.length < 8 && oldPassword.length > 0}">
                </div>
                <div class="field">
                    <input type="password" placeholder="New Password" v-model="password" :class="{'redify':!validatePassword && password.length > 0}">
                </div>
                <div class="field">
                    <input type="password" placeholder="Confirm Password" v-model="confirmPassword" :class="{'redify':(password != confirmPassword) && validatePassword}">
                </div>
                <div class="field">
                    <button @click="changePassword" class="bg-gradient-success text-white shadow-success" style="border:1px solid var(--bs-success);padding:.5rem 1rem;border-radius: .5rem;margin-top:2rem;" :disabled="(password != confirmPassword) || !validatePassword || oldPassword.length < 8">Change Password</button>
                </div>
              </div>
              
            </div>
          </div>
        </div>

        <div class="loading" v-if="isLoading">
            <div class="loader"></div>
        </div>
      </div>
</template>

<style lang="scss" scoped>
.field{
    margin:.5rem 0;
    width:100%;

    input{
        width:100%;
        padding:.2rem 1rem;
        border-radius: .2rem;
        border:1px solid var(--bs-gray);
    }
}

.loading{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;

    .loader{
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top-color: #343a40;
        border-radius: 50%;
        animation: spin 2s ease infinite;
    }
}

@keyframes spin {
    100%{
        transform: rotate(360deg);
    }
}

.close-button {
  margin-bottom:1.2rem;
  .svg-icon {
    cursor: pointer;
    svg {
      fill: #e32;
      width: 2rem;
      height: 2rem;
    }
  }
}

.fade{
  opacity: 0;
  animation:fadein .3s ease forwards;
}

@keyframes fadein {
  100%{
    opacity: 1;
  }
  
}

.redify{
  border: 2px solid var(--bs-danger) !important;
  outline: var(--bs-danger);
}

button:disabled{

  &:hover{
    opacity: 0.4 !important;
  }
  opacity: 0.4;
}
</style>
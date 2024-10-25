
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
const searchText = ref('');
const tableLoader = ref(false);
const trucks = ref(null);

const isCreateGateProcess = ref(false);
const selectedTruck = ref(null);
const visitation_purpose_type = ref('');


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

async function fetchTrucks(page=null, key=null){
    let params={}
    
    try {
    
    if(page){
        params.page = page;
    }
    if(key){
        params[key] = searchText.value;
        if(!searchText.value){
        return ;
        }
    }
    tableLoader.value=true;
    const response = await $http.get('/api/v1/trucks', {params});
    trucks.value = response.data;
    if(trucks.value.data.length == 0){
        toast.info("Truck Number not found",{
                        autoClose: 3000,
                        position: toast.POSITION.TOP_RIGHT,
                    })
                    this.err_msg = "Truck Number not Found !!"
    }
    tableLoader.value=false;
   isLoading.value=false;
    } catch (error) {
    tableLoader.value=false;
    isLoading.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(fetchTrucks);
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



async function submitCheck (update = false){
    const data = {
    visitation_purpose_type:visitation_purpose_type.value,
    truck_number:selectedTruck.value.truck_number
    }
    try{
    isLoading.value = true;
    let response = null;
    if(!update){
        response = await $http.post('api/v1/gateCheck', data)
    } else {
        response = await $http.put('api/v1/gateCheck', data)
    }
    if(response){
        isLoading.value = false;
        if(response.data.status){
        toast.success(response.data.message,{
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                    });
                    //this.fetchTrucks(null,'truck_number')
        selectedTruck.value=null;
        setisCreateGateProcess(false);
        trucks.value = null;
        searchText.value='';
        } else {
        toast.error(response.data.message,{
            autoClose: 3000,position: toast.POSITION.TOP_RIGHT,
        })
        
        }
    }
    }catch (error) {
        isLoading.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(submitCheck);
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



const setisCreateGateProcess = (val) => {
    isCreateGateProcess.value = val;
}
const selectTruck = (val) => {
    selectedTruck.value = val;
}

onMounted(() => {
    store.commit('setCurrentPage', 'gate-management')
    getUserData();
})

</script>


<template>
    <div class="container-fluid py-4">

        <div class="row">
          <div class="col-12">
            <div class="card my-4">
              <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                <div class="bg-gradient-secondary shadow-secondary border-radius-lg pt-4 pb-3">
                  <h6 class="text-white text-capitalize ps-3">Gate Security Check</h6>
                </div>
                <div class="searchbar my-3">
                    <input type="text" class="" @keyup.enter="fetchTrucks(null, 'truck_number')" v-model="searchText" placeholder="Truck Number" @input="searchText=searchText.toUpperCase()">
                    <button style="background:var(--bs-success);color:#fff;border:1px solid var(--bs-success);margin-left:10px;border-radius: .2rem;padding:.2rem 1rem;" @click="fetchTrucks(null, 'truck_number')">Search</button>
                </div>
              </div>
              <div class="card-body px-0 pb-2">
                <div class="table-responsive p-0">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Truck Number</th>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Brand Type</th>
                        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Driver Phone no.</th>
                   
                      </tr>
                    </thead>
                    
                    <tbody v-if="trucks && trucks.data.length > 0" >
                      <tr  style="cursor:pointer"  v-for="truck, index in trucks.data" :key="index" @click="selectTruck(truck);setisCreateGateProcess(true)">
                        <td>
                          <div class="d-flex px-2 py-1">
                            <div>
                              <img :src="truck.driver_image_url" class="avatar avatar-sm me-3 border-radius-lg" alt="user1" style="object-fit: cover;">
                            </div>
                            <div class="d-flex flex-column justify-content-center">
                              <h6 class="mb-0 text-sm">{{truck.truck_number}}</h6>
                              <p class="text-xs text-secondary mb-0">{{ truck.driver_name }}</p>
                            </div>
                          </div>
                        </td>
                        <td>
                          <p class="text-xs font-weight-bold mb-0">{{truck.brand_type}}</p>      
                        </td>
                        <td class="align-middle text-center text-sm">
                          <span class="badge badge-sm bg-gradient-success" v-if="truck.isCheckedIn">Checked In</span>
                          <span class="badge badge-sm bg-gradient-secondary" v-else>Checked Out</span>
                        </td>
                        <td class="align-middle text-center">
                          <span class="text-secondary text-xs font-weight-bold">{{truck.driver_phone_number}}</span>
                        </td>
                        
                      </tr>
                     
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        




        <div class="content-modal" v-if="isCreateGateProcess">
            <div class="modal-content">
              <div class="close-button">
                <span class="svg-icon"
                  ><svg
                    @click="isCreateGateProcess = false"
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
              <div id="reg">
                <form
                  class="add-gatein-form"
                  @submit.prevent="submitForm"
                  id="add-gatein-form"
                  ref="addgateinForm"
                >
                  <h3 class="title">Gate In Process Form </h3>
                  <h4 style="font-size:20px;width:100%;color:var(--dark);">Truck Info </h4>
                  <div class="imgbox" style="display:flex;width:100%;justify-content:center;align-items:center;overflow:hidden;margin:1rem 0;flex-direction: column;">
                    <img :src="selectedTruck.driver_image_url" alt="" style="object-fit: cover;border-radius: 50%;width:10rem;height:10rem;overflow:hidden" v-if="selectedTruck">
                    
                  </div>
                  <p style="width:100%;text-align: center;" v-if="selectedTruck">{{selectedTruck.driver_name}}</p>
                  <div class="field2 d-flex flex-column" style="margin-top:.5rem;" v-if="selectedTruck">
                    <label for="">Truck No.</label>
                    <input
                      type="text"
                      placeholder="Truck No."
                      v-model="selectedTruck.truck_number"
                      required
                      disabled
                      style="margin-top:-.5rem;font-size:18px"
                    />
                  </div>
                 
                  <div class="field2 d-flex flex-column" style="margin-top:.5rem;" v-if="selectedTruck && !selectedTruck.isCheckedIn">
                    <label for="">Visitation Purpose Type</label>
                    <select name="" id="" v-model="visitation_purpose_type" style="margin-top:-.5rem;">
                      <option value="" selected disabled>
                        Select Visitation Purpose Type
                      </option>
                      <option value="maintenance">Maintenance</option>
                      <option value="tyre collection">Tyre Collection</option>
                      <option value="tarpaulin collection">Tarpaulin Collection</option>
                      <option value="parking">Parking</option>
                    </select>
                  </div>
                  <div style="color:var(--dark);margin-top:1rem;" v-else>
                    
                    Visitation Purpose: <span style="color:var(--info-dark)">{{ selectedTruck.visitation_purpose_type }}</span>
                  </div>
                  
                </form>
                
                <p style="margin-top: 1rem;" v-if=" selectedTruck && selectedTruck.isCheckedIn">Check in Date: {{moment(selectedTruck.checkInDate).format("DD MMM YYYY, hh:mm  A")}}</p>
                
                <div v-if="selectedTruck">
                  <button @click="submitCheck();" v-if="!selectedTruck.isCheckedIn" style="background:var(--bs-success);">
                    Check In
                  </button>
                  
                  <button @click="submitCheck(true);" v-else style="background:var(--bs-danger)">
                    Check Out 
                  </button>
                </div>
              </div>
            </div>
      
      
            
          </div>
      
          <div class="loading" v-if="isLoading">
            <div class="loader"></div>
        </div>
      </div>
</template>


<style scoped lang="scss">

tr:hover{
    background-color:#eee;
}
select, input, textarea{
    color:var(--bs-dark);
    border:1px solid var(--bs-gray-dark) !important;
  }
.content-modal {
    display: flex;
    justify-content: center;
    padding: 1rem;
    padding-top: 5rem;
    width: 100%;
    height: 100%;
    background: #00000066;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999999;
  
    .modal-content {
      width: 100%;
      max-width: 30rem;
      height: fit-content;
      background: var(--bs-white);
      padding: 1rem;
      border-radius: .5rem;
      opacity: 0;
      animation: fadein 0.5s ease forwards;
  
      
  
      .close-button {
        .svg-icon {
          cursor: pointer;
          svg {
            fill: #e32;
            width: 2rem;
            height: 2rem;
          }
        }
      }
  
      .center-img {
        display: flex;
        width: 100%;
        justify-content: center;
        text-align: center;
        align-items: center;
      }
  
      button {
        border: 1px solid transparent;
        padding: 0.5rem 1rem;
        font-size: 16px;
        color: var(--bs-white);
        background: var(--bs-primary);
        border-radius: .5rem;
        margin-top: 2rem;
  
        &:hover {
          opacity: .8;
        }
      }
  
      .items {
        h3 {
          color: var(--bs-dark);
          text-transform: capitalize;
          font-size: 14px;
  
          &.title {
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            text-transform: uppercase;
          }
          span {
            color: var(--bs-dark);
            font-weight: 600;
          }
        }
      }
    
      .imgbox {
        width: 10rem;
        height: 10rem;
        position: relative;
        overflow: hidden;
        border-radius: 50%;
  
        margin-bottom: 1rem;
  
        img.profile {
          width: 100%;
  
          object-fit: cover;
        }
      }
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

.content-modal .modal-content .add-gatein-form {
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  
    .field,
    .field2 {
      display: flex;
      width: 100%;
    }
  
    input[type="text"],
    textarea,
    select {
      resize: none;
      width: 100%;
      margin: 0.2rem;
      padding: 0.5rem;
      border-radius: var(--border-radius-1);
      background: var(--light);
      color: var(--dark);
      margin-top: 0.5rem;
      border: 1px solid transparent;
    }
  }

@keyframes fadein {
    100%{
        opacity: 1;
    }
}

</style>
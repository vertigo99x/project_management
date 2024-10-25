
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
const recentMaintenanceChecklistLoader = ref(false);

const status = ref('pending');
const order = ref('');

const isCreateGateProcess = ref(false);
const confirmSubmitWorkOrder = ref(false);
const selectedTruck = ref(null);
const workOrders = ref(null);
const visitation_purpose_type = ref('');
const currentTabIndex = ref(0);
const currentList = ref(1);
const reg = ref(null);

const routineCount = ref(0);
const routinePagesCount = ref(0);
const totalNumberPerPage = ref(0);

const selectedTruckData = ref({
                electrical_system:"",
                air_cleaner:"",
                air_tank:"",
                water_filter:"",
                axle_hub_lubricant:"",
                coolant_level:"",
                transmission_oil_level:"",
                engine_oil_level:"",
                chassis_beams:null,
                kingpin:null,
                trailer_connecting_hose:null,
                hydrometer_and_diesel_tank:null,
                tractor_brake:null,
                transmission_fluid_level:null,
                gearbox_oil_level:null,
                axle_tank_and_disch_water:null,
                trailer_air_valve_leakage:null,
                wheel_studs:null,
                brake_lining:null,
                hub_covers:null,
                spring_center_bolt:null,
                equalizer:null,
                shock_absorbers:null,
                shackle_pins:null,
                overall_trailer_appearance:null,
                fan_belt_tension:null,
                pulley_for_clearance:null,
                tie_rod_clearance:null,
                oil_leakage:null,
                coolant_spills_leaks:null,
                air_cleaner_housing:null,
                air_leakage:null,
                dashboard_functions:null,
                air_pressure:null,
                oil_pressure:null,
                water_temperature:null,
                exhaust_leakage:null,
                front_shock_absorber:null,
                cab_barrel:null,
            })



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

async function getWorkOrders(recent=false, page=null, search=false) {
    recentMaintenanceChecklistLoader.value=true;
    
        try {
            const params = recent? {recent: recent} : {};
            params.status=status.value;
            if(page){
                params.page = page;
            }
            if(search && searchText.value){
                params.truck_number = searchText.value;
            }
            const response = await $http.get('api/v1/work-order', {params});
            workOrders.value = response.data;
            routineCount.value = 0;
            routinePagesCount.value = 0;
            totalNumberPerPage.value = workOrders.value.pagination.total_pages;
            if(workOrders.value.data.length >= totalNumberPerPage && workOrders.value.pagination.total_pages > 1){
                totalNumberPerPage.value = workOrders.value.data.length
            }

            recentMaintenanceChecklistLoader.value=false;
        } catch (error) {
        recentMaintenanceChecklistLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getWorkOrders);
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

async function submitWorkOrder(truckData) {
    if(status.value == 'pending'){
              //this.tableLoader=true;
          
              if(Object.keys(truckData).includes('value')){
            delete(truckData.value)
          }
          if(!selectedTruckData.electrical_system || !selectedTruckData.air_tank ||
                !selectedTruckData.air_cleaner || !selectedTruckData.water_filter ||
                !selectedTruckData.axle_hub_lubricant || !selectedTruckData.coolant_level ||
                !selectedTruckData.transmission_oil_level || !selectedTruckData.engine_oil_level
          ){
            toast.error("Fill in the required Fields", {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
                return ;
          }
    try {
        const data = {
            work_order_uuid:selectedTruck.value.uuid,
            work_order:truckData
        }
        const response = await $http.put('api/v1/work-order', data);
        document.querySelector(`#work-order${selectedTruck.value.uuid}`).remove()
        toast.info(response.data.message, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
        //tableLoader=false;
        confirmSubmitWorkOrder.value=false;
        resetCheckList();
        isCreateGateProcess.value=false;
        routineCount.value += 1;
        if(routineCount.value >= totalNumberPerPage.value / 2 && totalNumberPerPage > 1 && totalNumberPerPage.value > 1){
            getWorkOrders(order == 'recent'? true:false)
        }
    } catch (error) {
    
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(submitWorkOrder);
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
}




const setisCreateGateProcess = (val) => {
    isCreateGateProcess.value = val;
}

const selectTruck = (val) => {
    selectedTruck.value = val;
    if(status.value === 'completed'){
        selectedTruckData.value = val.work_order
        if(Object.keys(selectedTruckData.value).includes('value')){
            delete(selectedTruckData.value.value)
          }
        
    }
}

const resetCheckList = () => {
    visitation_purpose_type.value = ""
          currentTabIndex.value = 0
          currentList.value = 1
            selectedTruckData.value = {
                electrical_system:"",
                air_cleaner:"",
                air_tank:"",
                water_filter:"",
                axle_hub_lubricant:"",
                coolant_level:"",
                transmission_oil_level:"",
                engine_oil_level:"",
                chassis_beams:null,
                kingpin:null,
                trailer_connecting_hose:null,
                hydrometer_and_diesel_tank:null,
                tractor_brake:null,
                transmission_fluid_level:null,
                gearbox_oil_level:null,
                axle_tank_and_disch_water:null,
                trailer_air_valve_leakage:null,
                wheel_studs:null,
                brake_lining:null,
                hub_covers:null,
                spring_center_bolt:null,
                equalizer:null,
                shock_absorbers:null,
                shackle_pins:null,
                overall_trailer_appearance:null,
                fan_belt_tension:null,
                pulley_for_clearance:null,
                tie_rod_clearance:null,
                oil_leakage:null,
                coolant_spills_leaks:null,
                air_cleaner_housing:null,
                air_leakage:null,
                dashboard_functions:null,
                air_pressure:null,
                oil_pressure:null,
                water_temperature:null,
                exhaust_leakage:null,
                front_shock_absorber:null,
                cab_barrel:null,
            }
}

const setCurrentTabIndex = (number) => {
    currentTabIndex.value = number
}

const modalScrollTop = () => {
    reg.value.scrollTo(0,0)
}

const selectedRoutineRow = (item) => {
    if(status.value === 'pending' || status.value === 'completed'){
        resetCheckList();
        selectTruck(item);
        setCurrentTabIndex(1);
        setisCreateGateProcess(true);
    }
}

onMounted(() => {
    store.commit('setCurrentPage', 'routine-maintenance')
    getUserData();
    getWorkOrders();
})


</script>


<template>
    <div class="container-fluid py-4" v-if="userData">

        <div class="row">
          <div class="col-12">
            <div class="card my-4">
              <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                <div class="bg-gradient-secondary  border-radius-lg pt-4 pb-3">
                  <h6 class="text-white text-capitalize ps-3">
                    <span>{{status}}</span>
                    Routine Maintainance Checklist
                  </h6>
                </div>
                <div class="searchbar my-3">
                    <input type="text" class="" @keyup.enter="fetchTrucks(null, 'truck_number')"  v-model="searchText" placeholder="Search Table" >
                    <button style="background:var(--bs-success);color:#fff;border:1px solid var(--bs-success);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="getWorkOrders(order == 'recent'? true:false,null,true)">Search</button>
                    <button style="background:var(--bs-secondary);color:#fff;border:1px solid var(--bs-secondary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" class="reset-table" @click="status='pending';order='';searchText='';getWorkOrders(order == 'recent'? true:false,null,false)">Reset Table</button>
                    
                    
                </div>
                <div class="searchbar my-3">
                    <select name="" id="" v-model="status" @change="getWorkOrders(order == 'recent'? true:false)">
                        <option value="pending">Pending Routine Checklist</option>
                        <option value="completed">Completed Routine Checklist</option>
                        <option value="cancelled">Cancelled Routine Checklist</option>
                      </select>
                      <select class="mx-2" id="" v-model="order" @change="getWorkOrders(order == 'recent'? true:false)">
                        <option value=""> Sort By Oldest</option>
                        <option value="recent">Sort By Most Recent</option>
                       
                      </select>
                    
                </div>
              </div>

              <div class="card-body px-0 pb-2">
                <div class="table-responsive p-0">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Truck Number</th>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Truck Brand</th>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Date In</th>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2" v-if="userData.role == 'admin' && (status=='completed' || status=='cancelled')">Maintenance Supervisor</th>
                        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7" v-if="status=='completed'">Checklist Date</th>
                        <th class="text-secondary opacity-7"></th>
                      </tr>
                    </thead>
                    
                    <tbody v-if="workOrders && workOrders.data.length > 0" >
                      <tr  style="cursor:pointer"  v-for="item, index in workOrders.data" :key="index" @click="
                      selectedRoutineRow(item);
                      " :id="'work-order'+item.uuid">
                        <td>
                          <div class="d-flex px-2 py-1">
                            
                            <div class="d-flex flex-column justify-content-center">
                              <h6 class="mb-0 text-sm">{{item.truck.truck_number}}</h6>
                              <p class="text-xs text-secondary mb-0">{{ item.truck.driver_name }}</p>
                            </div>
                          </div>
                        </td>
                        <td>
                          <p class="text-xs font-weight-bold mb-0">{{item.truck.brand_type}}</p>      
                        </td>
                        <td>
                          <p class="text-xs font-weight-bold mb-0">{{moment(item.date_added).format("DD MMM, YYYY. hh:mm A") }}</p>      
                        </td>
                        <td v-if="(status=='completed' || status=='cancelled') && userData.role=='admin'">
                            <div class="d-flex px-2 py-1">
                              
                              <div class="d-flex flex-column justify-content-center">
                                <h6 class="mb-0 text-sm">{{ item.maintenance_supervisor.last_name }} {{ item.maintenance_supervisor.first_name }}</h6>
                                <p class="text-xs text-secondary mb-0">{{ item.maintenance_supervisor.email }}</p>
                              </div>
                            </div>
                          </td>
                        <td class="align-middle text-center text-sm">
                            <span class="badge badge-sm bg-gradient-success" v-if="item.status=='completed'">{{ item.status}}</span>
                            <span class="badge badge-sm bg-gradient-danger" v-else-if="item.status=='cancelled'">{{ item.status }}</span>
                            <span class="badge badge-sm bg-gradient" style="background:var(--bs-orange);" v-else>{{ item.status }}</span>
                          </td>
                        <td class="align-middle text-center" v-if="status=='completed'">
                          <span class="text-secondary text-xs font-weight-bold" >{{moment(item.checklist_upload_date).format("DD MMM, YYYY. hh:mm A")}}</span>
                        </td>
                        
                      </tr>
                     
                    </tbody>
                  </table>
                  <div class="pagination"  v-if="workOrders">

                    <div class="controls" v-if="workOrders.pagination">
                     <span @click="getWorkOrders(order == 'recent'? true:false, workOrders.pagination.current_page - 1)"  v-if="workOrders.pagination.current_page > 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span  v-else-if="workOrders.pagination.total_pages !== 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span v-for="i in workOrders.pagination.total_pages" :key="i" @click="getWorkOrders(order == 'recent'? true:false, i)" :class="{'active':workOrders.pagination.current_page === i}">
                       {{ i }}
                     </span>
                     <span @click="getWorkOrders(order == 'recent'? true:false, workOrders.pagination.current_page + 1)" v-if="workOrders.pagination.current_page < workOrders.pagination.total_pages">
                       <i class="material-icons">chevron_right</i>
                     </span>
                    </div>
                 
                     <div class="pagination-info">
                       <span>Page {{ workOrders.pagination.current_page }} of {{ workOrders.pagination.total_pages }}</span>
                     </div>
                   </div>
                  <div class="table-loader" v-if="recentMaintenanceChecklistLoader">
                    <div class="loader"></div>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        




        <div class="content-modal" v-if="isCreateGateProcess">
            <div class="modal-content" v-if="currentTabIndex == 0">
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
                  <h3 class="title">Gate In Process Form</h3>
                  <div class="field2 d-flex flex-column" style="margin-top:.5rem;">
                    <label for="">Truck No.</label>
                    <input
                      type="text"
                      placeholder="Truck No."
                      :value="selectedTruck.truck.truck_number"
                      required
                      disabled
                      style="margin-top:-.5rem;font-size:18px"
                    />
                  </div>
                  <div class="field2 d-flex flex-column" style="margin-top:.5rem;">
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
                </form>
                <button @click="this.currentTabIndex = 1;" v-if="visitation_purpose_type == 'maintenance'">
                  Generate Work Order <i class="fa-solid fa-list-check"></i>
                </button>
                <button @click="next();" v-else>
                  Next <i class="material-icons"></i>
                </button>
              </div>
            </div>
      
      
            <div class="modal-content" id="multi-modal"  style="max-width:55rem;width:100%;" v-if="currentTabIndex == 1">
              <div class="close-button">
                <span class="svg-icon"
                  ><svg
                    @click="resetCheckList();isCreateGateProcess = false"
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
              <div id="reg" ref="reg" class="reg" :class="{'completed':status=='completed'}">
                <form
                  class="add-gatein-form"
                  @submit.prevent="submitForm"
                  id="add-gatein-form"
                  ref="addgateinForm"
                >
                <h3 class="title">Fault Recording</h3>
                <div class="page-marker">
                    
                  <ul id="progressbar">
                    <li :class="{'active':currentList>=1}">Routine Maintenance Checklist </li>
                    <li :class="{'active':currentList>=2}">Chassis</li>
                    <li :class="{'active':currentList>=3}">Semi Trailers</li>
                    <li :class="{'active':currentList>=4}">Engine/Cabin</li>
                  </ul>
                </div>
      
                  
                  <div class="field2" style="display:flex;flex-direction:column;">
                    
                    <label for="" style="font-weight:bold;font-size: 18px;">Truck No.</label>
                    <input
                      type="text"
                      placeholder="Truck No."
                      :value="selectedTruck.truck.truck_number"
                      required
                      disabled
                      id="truck-no"
                      style="font-weight:bold;font-size: 18px;color:var(--primary);letter-spacing:1px"
                    />
                   
                  </div>
                  
                  <div class="list-1" v-if="currentList==1">
                    <h4 style="margin:2rem 0 1rem 0;font-weight:600;">Routine Maintenance Checklist</h4>
      
                    <div class="field2">
                      <div class="checklist">
                        <label for="">&nbsp;Electrical System </label>
                        <select name="" id="" v-if="status=='pending'" :disabled="status=='completed'" v-model="selectedTruckData.electrical_system">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.electrical_system.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      <div class="checklist">
                        <label for="">&nbsp;Air Cleaner</label>
                        <select name="" id="" v-if="status=='pending'" :disabled="status=='completed'" v-model="selectedTruckData.air_cleaner">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.air_cleaner.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      <div class="checklist">
                        <label for="">&nbsp;Air Tank</label>
                        <select name="" id="" v-if="status=='pending'" :disabled="status=='completed'" v-model="selectedTruckData.air_tank">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.air_tank.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      <div class="checklist">
                        <label for="">&nbsp;Water Filter</label>
                        <select name="" id="" v-if="status=='pending'"  :disabled="status=='completed'" v-model="selectedTruckData.water_filter">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.water_filter.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      
                    </div>
                    
                    <div class="field2">
                      <div class="checklist">
                        <label for="">&nbsp;Axle Hub Lubricant</label>
                        <select name="" id="" v-if="status=='pending'" :disabled="status=='completed'" v-model="selectedTruckData.axle_hub_lubricant">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.axle_hub_lubricant.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      <div class="checklist">
                        <label for="">&nbsp;Coolant Level</label>
                        <select name="" id=""  v-if="status=='pending'" :disabled="status=='completed'" v-model="selectedTruckData.coolant_level">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.coolant_level.replace('_',' ') || "None"}}</p>
                     
                      </div>
                      <div class="checklist">
                        <label for="">&nbsp;Transmission Oil Level</label>
                        <select name="" id="" v-if="status=='pending'"  :disabled="status=='completed'" v-model="selectedTruckData.transmission_oil_level">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="">Maintenance</option>
                          <option value="">Tyre Collection</option>
                          <option value="">Tarpaulin Collection</option>
                          <option value="">Parking</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.transmission_oil_level.replace('_',' ') || 'None'}}</p>
                     
                      </div>
                      <div class="checklist" >
                        <label for="">&nbsp;Engine Oil Level</label>
                        <select name="" id="" v-if="status=='pending'"  :disabled="status=='completed'" v-model="selectedTruckData.engine_oil_level">
                          <option value="" selected disabled>
                            Select Option
                          </option>
                          <option value="replaced">Replaced</option>
                          <option value="topped_up">Topped Up</option>
                          <option value="bled">Bled</option>
                          <option value="blown">Blown</option>
                          <option value="checked">Checked</option>
                          <option value="yes">Yes</option>
                          <option value="no">No</option>
                        </select>
                        <p v-else style="color:var(--bs-primary);text-transform:capitalize;text-align:center;">{{selectedTruckData.engine_oil_level.replace('_',' ') || "None"}}</p>
                      </div>
                      
                    </div>
      
                    <div class="buttonbox">
                      <button style="" class="ghost-button">
                        
                      </button>
                      <button @click="currentList = 2;modalScrollTop()" class="next-page">
                        Next Page <i class="material-icons"></i>
                      </button>
                    </div>
                  </div>
                  
                  
                  <div class="list-2" v-if="currentList==2">
                    <h4 style="margin:2rem 0 1rem 0;font-weight:600;">Chassis</h4>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                      <label for="">&nbsp;Chassis Beams</label>
                      <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.chassis_beams">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                      <label for="">&nbsp;Kingpin</label>
                      <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.kingpin">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Trailer Connecting Hose</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.trailer_connecting_hose">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Hydrometer & Diesel Tank</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.hydrometer_and_diesel_tank">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    
                  </div>
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Tractor Brake</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.tractor_brake">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Transmission Fluid Level</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.transmission_fluid_level">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Gearbox Oil Level</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.gearbox_oil_level">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Axle Tank & Disch. Water</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.axle_tank_and_disch_water">
                        <span class="custom-checkbox"></span>
                    </div>
                  </div>
                  <div class="buttonbox">
                    <button @click="currentList = 1;modalScrollTop()">
                     <i class="material-icons"></i> Back 
                    </button>
                    <button @click="currentList = 3;modalScrollTop()" class="next-page">
                      Next Page <i class="material-icons"></i>
                    </button>
                  </div>
                  </div>
      
      
                  <div class="list-3" v-if="currentList==3">
                    <h4 style="margin:2rem 0 1rem 0;font-weight:600;">Semi Trailer</h4>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Trailer Air Valve Leakage</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.trailer_air_valve_leakage">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Wheel Studs</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.wheel_studs">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Brake Lining</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.brake_lining">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Hub Covers</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.hub_covers">
                        <span class="custom-checkbox"></span>
                    </div>                            
                  </div>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Spring/Center Bolt</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.spring_center_bolt">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Equalizer</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.equalizer">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Shock Absorbers</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.shock_absorbers">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Shackle Pins</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.shackle_pins">
                        <span class="custom-checkbox"></span>
                    </div>  
                    </div>          
                  
                  <div class="field2 check">
                    <div class="checklist-check">
                      <label for="">&nbsp;Overall Trailer Appearance</label>
                      <input type="checkbox" name="" id="">
                        <span class="custom-checkbox"></span>
                    </div>      
                    <div class="checklist-check exempt-b"></div>      
                    <div class="checklist-check exempt-b"></div>      
                    <div class="checklist-check exempt-b"></div>      
                  </div>
      
                  <div class="buttonbox">
                    <button @click="currentList = 2;modalScrollTop()">
                       <i class="material-icons"></i>Back
                    </button>
                    <button @click="currentList = 4;modalScrollTop()" class="next-page">
                      Next Page <i class="material-icons"></i>
                    </button>
                  </div>
                </div>
                
                  
                  <div class="list-4" v-if="currentList==4">
                    <h4 style="margin:2rem 0 1rem 0;font-weight:600;">Engine/Cabin</h4>
                  
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Fan Belt Tension</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.fan_belt_tension">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Pulley for Clearance</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.pulley_for_clearance">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Tie Rod Clearance</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.tie_rod_clearance">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Oil Leakage</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.oil_leakage">
                        <span class="custom-checkbox"></span>
                    </div>                         
                  </div>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Coolant Spills/Leaks</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.coolant_spills_leaks">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Air Cleaner Housing</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.air_cleaner_housing">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Air Leakage</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.air_leakage">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Dashboard Functions</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.dashboard_functions">
                        <span class="custom-checkbox"></span>
                    </div>
                  </div>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Air Pressure</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.air_pressure">
                        <span class="custom-checkbox"></span>
                    </div>
                   
                    <div class="checklist-check">
                        <label for="">&nbsp;Oil Pressure</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.oil_pressure">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Water Temperature</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.water_temperature">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check">
                        <label for="">&nbsp;Exhaust Leakage</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.exhaust_leakage">
                        <span class="custom-checkbox"></span>
                    </div>      
                  </div>
      
                  <div class="field2 check">
                    <div class="checklist-check">
                        <label for="">&nbsp;Front Shock Absorber</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.front_shock_absorber">
                        <span class="custom-checkbox"></span>
                    </div>

                    <div class="checklist-check">
                        <label for="">&nbsp;Cab Barrel</label>
                        <input type="checkbox" name="" id=""  :disabled="status=='completed'" v-model="selectedTruckData.cab_barrel">
                        <span class="custom-checkbox"></span>
                    </div>
                    <div class="checklist-check exempt-b"></div>      
                    <div class="checklist-check exempt-b"></div>      
                              
                  </div>
                  <div class="buttonbox">
                    <button @click="currentList = 3;modalScrollTop()">
                       <i class="material-icons"></i>Back
                    </button>
                    <button class="next-page" @click="confirmSubmitWorkOrder=true" v-if="status=='pending'">
                      Submit <i class="material-icons"></i>
                    </button>
                  </div>
                  </div>
      
                </form>
                
              </div>
            </div>
          </div>
          
          <div class="content-modal" v-if="confirmSubmitWorkOrder">
            <div class="modal-content">
              <h2>Confirm Routine Checklist?</h2>
              <p>Are you sure you want to submit the result of this checklist?</p>
              <div class="buttonbox" style="display: flex;justify-content: space-between;">
                <button @click="confirmSubmitWorkOrder=false;currentList=1;modalScrollTop()" style="background-color: var(--bs-danger);">Cancel</button>
                <button @click="submitWorkOrder(selectedTruckData)" class="bg-success" style="">Submit</button>
              </div>
             
            </div>
    
          </div>
      
          <div class="loading" v-if="isLoading">
            <div class="loader"></div>
        </div>
      </div>
</template>


<style scoped lang="scss">
select, input, textarea{
    color:var(--bs-dark);
    border:1px solid var(--bs-gray) !important;
    border-radius: .5rem;
    padding:.2rem .5rem;
  }


  body.dark-version .modal-content{
    background: #161B1D;
    color: var(--bs-white);
    input{
        color:var(--bs-dark) !important;
    }
    
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
      border-radius: .5rem;
      background: var(--bs-light);
      color: var(--bs-dark);
      margin-top: 0.5rem;
      border: 1px solid transparent;
    }
  }

  .table-loader{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-color: rgba(0,0,0,0.25);
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;

    .loader{
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top-color: #343a40;
        border-radius: 50%;
        animation: spin 1s cubic-bezier(0.445, 0.05, 0.55, 0.95) infinite;
    }
}

.pagination{
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
    padding:.5rem 1rem;
  
    .controls{
      display:flex;
  
      span{
        display:flex;
        align-items: center;
        justify-content: center;
        padding:.5rem;
        margin:.2rem;
        width:30px;
        height:30px;
        overflow: hidden;
        border-radius:50%;
        font-size:18px;
        cursor:pointer;
  
        &:disabled, &.disabled{
          color:#888;
        }
    
        &.active{
          background-color: var(--bs-primary);
          color: var(--bs-light);
          cursor:default;
        }
        &:not(.active):hover {
          background-color: rgba(0,0,0,0.25);
          color: var(--bs-light);
          cursor: pointer;
        }
      }
    }
  
    
  }

.table-responsive{
    position: relative;
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
@keyframes fadein {
    100%{
        opacity: 1;
    }
}

button:disabled {
    opacity: 0.6;
  }

  
.checklist{
    padding:.5rem;
    display: grid;
  
    select{
      margin-top:-3.5rem;
    }
  }

.upload-div {
    .image-show {
      width: 100%;
      justify-content: center;
      display: flex;
      position: relative;
  
      img {
        width: 150px;
        height: 150px;
  
        object-fit: cover;
      }
    }
  
    .title {
      margin: 1rem 0 2rem 0;
      text-transform: capitalize;
      font-weight: 600;
      color: var(--bs-dark);
    }
  
    p {
      color: var(--bs-dark);
      margin-top: 2rem;
    }
  
    .form-data {
      width: 100%;
      position: relative;
  
      .field {
        width: 100%;
        display: grid;
        grid-auto-flow: column;
        grid-template-columns: 30% 70%;
        margin: 0.5rem 0;
        align-items: center;
  
        &:not(:last-child) {
        }
  
        input[type="text"],
        input[type="number"],
        select {
          padding: 0.5rem;
          max-height: 40px;
          border: 1px solid transparent;
          border-radius: .2rem;
          background: var(--bs-light);
          color: var(--bs-dark);
  
          :disabled {
            text-transform: uppercase;
            font-weight: 600;
          }
        }
      }
    }
  }
  



.list-1, .list-2, .list-3, .list-4{
    opacity: 0;
    animation: fadein .5s ease forwards;
    width:100% !important;
  
    .buttonbox{
      display: flex;
      justify-content: space-between;
      padding:.5rem;
  
      .ghost-button{
        cursor:default;
        background:transparent;
        color:transparent;
        display: block;
      }
    }
  
    button{
      border-radius:.2rem !important;
  
      &.next-page{
        background: var(--bs-secondary);
        color: var(--bs-white);
        border: 1px solid var(--bs-secondary);
  
        &:hover{
          background: var(--bs-white);
          color: var(--bs-secondary);
          border: 1px solid var(--bs-secondary);
        }
      }
    }
  }
  
  


  .page-marker{
    width:100%;
    padding: 1rem;
   
  }
  
  /*progressbar*/
  #progressbar {
    margin: 1rem;
    display: flex;
    justify-content: center;
    width: 100%;
    overflow: hidden;
    padding:0;
    /*CSS counters to number the steps*/
    counter-reset: step;
  }
  #progressbar li {
    list-style-type: none;
    color: var(--bs-secondary);
    text-transform: uppercase;
    font-size: 12px;
    text-align: center;
    width: 20%;
    float: left;
    position: relative;
  }
  #progressbar li:before {
    content: counter(step);
    counter-increment:step;
    width: 40px;
    height: 40px;
    line-height: 40px;
    
    display: block;
    font-size: 16px;
    color: var(--bs-white);
    background: var(--bs-secondary);
    border-radius: .2rem;
    margin: 0 auto 5px auto;
  }
  /*progressbar connectors*/
  #progressbar li:after {
    content: "";
    width: 100%;
    height: 2px;
    background: var(--bs-primary);
    position: absolute;
    left: -50%;
    top: 20px;
    z-index: -1; 
  }
  #progressbar li:first-child:after {
    /*connector not needed before the first step*/
    content: none;
  }
  /*marking active/completed steps green*/
  /*The number of the step and the connector before it = green*/
  #progressbar li.active:before,
  #progressbar li.active:after {
    background: var(--bs-primary);
    color: var(--bs-white);
  }
  
  
  
  .field2.check{
    display: grid;
    grid-auto-flow: column;
    grid-template-columns: 25% 25% 25% 25%;
    width:100%;
    
  }
  
  .checklist-check{
   
    width:100%;
    display: flex;
    align-items:center;
    
    
    padding:.5rem 1rem;
    
    
  
    input[type="checkbox"]{
      
      width:2rem;
      height:2rem;
      margin:0;
      padding:0;
      margin-left: .5rem;
      margin-top: -.5rem;
      
    }
  
    label, p{
      font-size:14px;
      font-weight:400;
      color:var(--bs-dark);
      width:100%;
      text-transform: capitalize;
      
    }
  }
  
  #truck-no{
    width:30%;
  }
  

  .add-gateins {
    margin: 1rem 0;
    border-radius: .2rem;
    border: 2px dotted rgb(224, 104, 58);
    padding: 0.5rem 1rem;
    font-size: 14px;
    color: var(--white);
    background: rgb(224, 104, 58);
    cursor: pointer;
  
    &:hover {
      color: rgb(224, 104, 58);
      background: var(--bs-white);
    }
  }
  

  .completed{
    
  input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }

  /* Create a custom checkbox */
  .custom-checkbox {
    position: relative;
    display: inline-block;
    width: 35px;
    height: 30px;
    background-color: #ededed;
    
    border-radius: 5px;
  }

  /* Add a checkmark when checked */
  .custom-checkbox:after {
    content: "";
    position: absolute;
    display: none;
    left: 11px;
    top: 9px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg);
  }

  /* Show the checkmark when the checkbox is checked */
  input[type="checkbox"]:checked ~ .custom-checkbox {
    background-color: var(--bs-success);
  }

  input[type="checkbox"]:checked ~ .custom-checkbox:after {
    display: block;
  }

  }



















  
@media screen and (max-width: 600px) {


    .searchbar:nth-child(3){
        display:flex;
        flex-direction: column;

        select{
            width:100%;
            margin:.5rem 0 !important;
            padding:0;

        }

    }
    .pagination{
      flex-direction:column;
      
      .controls{
        margin-top:1rem;
      }

      .pagination-info{
        margin-top: 1rem;
      }
    }
    .modal-content {
      #reg {
        overflow-y: auto;
        max-height: 40rem;
        
       
      }
      
      button {
        width: 100%;
      }
    }
    .content-modal .modal-content .add-gatein-form {
      input {
        width: 100%;
      }
      .field, .field2 {
        flex-direction: column;
        width: 100%;
      }
  
      .field2{
        &:first-child{
          
        }
        .checklist-check:not(.exempt-b){
          border-bottom:1px solid var(--bs-light);
          padding:0;
          margin:.5rem 0;
        }   
        
        .exempt-b{
          display:none;
        }
      }
      .list-1, .list-2, .list-3, .list-4{
        .buttonbox{
          display: flex;
          flex-direction: column;
  
          button, .next-page{
            width: 100%;
            padding:.5rem;
            font-size: 14px;
            
            
          }
          .ghost-button{
            display:none !important; 
          }
        }
      }
      
      .page-marker{
        padding:0;
        display: flex;
        position: relative;
        top:0;
        left:0;
        background:var(--bs-white) !important;
        z-index: 99;
        
      }
  
      #progressbar{
        width:100%;
        margin:1rem 0;
        margin-bottom:2rem;
        
        left:0;
     
        
      }
      #truck-no{
        width:100%;
      }
     
    }
  
    .head{
      display:flex;
      flex-direction: column;
      align-items:flex-start !important;
      justify-content: flex-start !important;
      
      .search input{
        width:100% !important;
      }
    }
    
  }
  
  .head select{
    background-color:var(--info-light);
    border:none;
    border-radius:.5rem;
    padding:10px;
  }
  
  @media screen and (max-width: 400px){
    .modal-content {
      #reg {
        overflow-y: auto;
        max-height: 30rem;
      }
      button {
        width: 100%;
      }
    }
    
  }


  

</style>
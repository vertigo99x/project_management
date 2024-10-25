
<script setup>
import { ref, inject, onMounted, onBeforeUnmount } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import moment from 'moment';
import axios from 'axios';

import MiddleCharts from '../components/MiddleCharts.vue';

const $http = inject('$http');
const router = useRouter();
const route = useRoute();
const store = useStore();

const isLoading = ref(false);
const recentMaintenanceChecklistLoader = ref(false);
const recentProjectsLoader = ref(false);
const recentActivitiesLoader = ref(false);

const userData = ref(null);
const dashboardData = ref(null);
const gateProcess = ref(null);
const projects = ref(null);
const activities = ref(null);


let timer = null;




async function refreshToken(callback) {
    try {
        const response = await $http.post('api/token/refresh', {
            refresh: store.getters.refresh,
        });

        if (response.data.access) {
            store.commit('setAccess', response.data.access);
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            await callback();  
        } else {
            router.push('/login');  
        }
    } catch (error) {
        console.error('Failed to refresh token', error);
        router.push('/login');  
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
            } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                toast.error(`Too many requests. try again in a minute`, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
                setTimeout(() => {
                    getUserData();
                }, 60000);

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

async function getDashboardData(loader=true) {
    if(loader){
        isLoading.value = true;
    } else{
        isLoading.value = false;
    }
    try {
        const response = await $http.get('api/v1/dashboard');
        dashboardData.value = response.data;
        isLoading.value = false;
    } catch (error) {
    isLoading.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(getDashboardData);
            } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                console.error(`Too many requests. try again in a minute`)
                if(!timer){
                    clearInterval(timer);
                    timer=null;
                    setTimeout(() => {
                        autoReload();
                    }, 60000)
                }
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

async function getGateProcess(recent=true) {
    recentMaintenanceChecklistLoader.value = true;
    try {
        const params = recent? {recent: recent} : {};
        const response = await $http.get('api/v1/gateCheck', {params});
        gateProcess.value = response.data.data.slice(0,10);
        recentMaintenanceChecklistLoader.value = false;
    } catch (error) {
    recentMaintenanceChecklistLoader.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(getGateProcess);
            } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                setTimeout(() => {
                    getGateProcess(recent=recent);
                }, 60000);
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

async function getProjects(page=null, extraparams=null){
    let params = {}
    recentProjectsLoader.value=true;
    try{
        if (page){
        params.page=page;
        }
        if(extraparams){
        params = {...params,...extraparams}
        }

        const response = await $http.get('api/v1/projects', {params})
        projects.value = response.data
        recentProjectsLoader.value=false;

    } catch (error){
        recentProjectsLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getProjects);
                } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                console.error(`Too many requests. try again in a minute`)
                setTimeout(() => {
                    getProjects(page, extraparams);
                }, 60000);
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

async function getActivities(loader=true) {
    if(loader){
        recentActivitiesLoader.value = true;
    } else{
        recentActivitiesLoader.value = false;
    }
        try {
            const response = await $http.get('api/v1/activities');
            activities.value = response.data.data;
            recentActivitiesLoader.value = false;
        } catch (error) {
        recentActivitiesLoader.value = false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getActivities);
                } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                console.error(`Too many requests. try again in a minute`)
                if(!timer){
                    clearInterval(timer);
                    timer=null;
                    setTimeout(() => {
                        autoReload();
                    }, 60000)
                }
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



async function getAppData(){
    getUserData();
    //getDashboardData();
    //getGateProcess();
    getProjects();
    //getActivities();
}



const isSmallSize = () => {
  return window.innerWidth <= 786;
}

const isWithinOneHour = (time) => {
    const currentTime = new Date();
    const maintenanceTime = new Date(time);
    maintenanceTime.setHours(maintenanceTime.getHours() + 1);
    return currentTime <= maintenanceTime;

}

const autoReload = () => {
    if(!timer){
        timer = setInterval(() => {
            getDashboardData(false);
            getActivities(false);
        }, 5000)
    }
}

onMounted(() => {
    store.commit('setCurrentPage', 'dashboard')
    getAppData();
    //autoReload();
});

onBeforeUnmount(() => {
    clearInterval(timer);
})

</script>

<template>
    
    <div class="container-fluid py-4" v-if="userData">
      

        <div class="" style="margin:0 2rem 3rem 2rem;" v-if="isSmallSize() && userData.role=='security_officer'">
            <router-link to="security" class="bg-gradient-info shadow-info text-white " style="border:1px solid var(--bs-blue); padding:.5rem 1rem;border-radius: .5rem;">Gate Management</router-link>
        </div>
     
        <div class="row" v-if="userData.role == 'security_officer' && dashboardData">
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-dark shadow-dark text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">local_shipping</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Trucks In</p>
                    <h4 class="mb-0">{{dashboardData.data.gateChecks.trucks_in}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder"></span>since 24 hrs ago</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-primary shadow-primary text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10" style="transform: scaleX(-1);">local_shipping</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Trucks Out</p>
                    <h4 class="mb-0">{{dashboardData.data.gateChecks.trucks_out}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder"></span>Since 24hrs ago</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-info shadow-info text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10" style="transform: scaleX(-1);">factory</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Trucks in Premises</p>
                    <h4 class="mb-0">{{dashboardData.data.gateChecks.trucks_in_premises}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder"></span>Total trucks still in Premises</p>
                </div>
              </div>
            </div>
            
        </div>

        <div class="row" v-else-if="userData.role == 'maintenance_supervisor' && dashboardData">
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-dark shadow-dark text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">pending</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Pending Routine Checks</p>
                    <h4 class="mb-0">{{dashboardData.data.workOrderCount}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0" style="color:transparent;"><span class="text-success text-sm font-weight-bolder"></span>Routine walk-around check</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-primary shadow-primary text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">person</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Assigned Jobs</p>
                    <h4 class="mb-0">{{dashboardData.data.assignedJobs}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder"></span>since 24 hrs ago</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-info shadow-success text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">person</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Jobs in Progress</p>
                    <h4 class="mb-0">{{dashboardData.data.activeJobs}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-danger text-sm font-weight-bolder"></span>Current Number of Active Jobs</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-success shadow-info text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">done_all</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Completed Jobs</p>
                    <h4 class="mb-0">{{dashboardData.data.completedJobs}}</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder"></span>since 24 hrs ago.</p>
                </div>
              </div>
            </div>
        </div>
        
        <div class="row" v-else-if="userData.role == 'admin' && dashboardData">
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-dark shadow-dark text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">weekend</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Total Trucks in Premises</p>
                    <h4 class="mb-0">$53k</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder">+55% </span>than last week</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-primary shadow-primary text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">person</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Total Jobs in Progress</p>
                    <h4 class="mb-0">2,300</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder">+3% </span>than last month</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-success shadow-success text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">person</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Active Technicians</p>
                    <h4 class="mb-0">3,462</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-danger text-sm font-weight-bolder">-2%</span> than yesterday</p>
                </div>
              </div>
            </div>
            <div class="col-xl-3 col-sm-6">
              <div class="card">
                <div class="card-header p-3 pt-2">
                  <div class="icon icon-lg icon-shape bg-gradient-info shadow-info text-center border-radius-xl mt-n4 position-absolute">
                    <i class="material-icons opacity-10">weekend</i>
                  </div>
                  <div class="text-end pt-1">
                    <p class="text-sm mb-0 text-capitalize">Sales</p>
                    <h4 class="mb-0">$103,430</h4>
                  </div>
                </div>
                <hr class="dark horizontal my-0">
                <div class="card-footer p-3">
                  <p class="mb-0"><span class="text-success text-sm font-weight-bolder">+5% </span>than yesterday</p>
                </div>
              </div>
            </div>
        </div>

          <div class="row mt-4">
           <MiddleCharts :userData="userData" v-if="userData.role == 'admin'" />
          </div>

          <div class="row mb-4">
            <div class="col-lg-8 col-md-12 mb-md-0 mb-4">






              <div class="card">
                <div class="card-header pb-0">
                  <div class="row">
                    <div class="col-lg-6 col-md-6 col-7">
                      <h6 v-if="userData.role=='admin'">Recently Created Projects</h6>
                      <h6 v-else>Recently Assigned Projects</h6>
                    </div>
                    <div class="col-lg-6 col-5 my-auto text-end d-lg-block text-sm" v-if="userData.role=='admin'">
                        <span style="text-decoration: underline;color:var(--bs-blue);cursor:pointer">View All</span>
                    </div>
                    <div class="col-lg-6 col-5 my-auto text-end d-none" >
                      <div class="dropdown float-lg-end pe-4">
                        <a class="cursor-pointer" id="dropdownTable" data-bs-toggle="dropdown" aria-expanded="false">
                          <i class="fa fa-ellipsis-v text-secondary"></i>
                        </a>
                        <ul class="dropdown-menu px-2 py-3 ms-sm-n4 ms-n5" aria-labelledby="dropdownTable">
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Action</a></li>
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Another action</a></li>
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Something else here</a></li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="card-body px-0 pb-2">
                   <div class="table-responsive">
                    <table class="table align-items-center mb-0">
                      <thead>
                        <tr>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Project Name</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">project description</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7" v-if="userData.role=='admin'">Assigned to</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">status</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">priority</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">date created</th>

                        </tr>
                      </thead>
                      <tbody v-if="projects">
                        <tr v-for="item in projects.data" :key="item">
                          <td>
                            <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-primary);">
                                {{item.project_name}}
                            </div>
                          </td>
                          <td class="text-sm">
                            {{item.project_description.length >=25 ? item.project_description.slice(0,25) : item.project_description}}
                          </td>
                          <td class="align-middle text-center text-sm" v-if="userData.role=='admin'">
                            <span class="text-xs font-weight-bold" v-if="item.assigned_to">{{ item.assigned_to.last_name}} {{ item.assigned_to.first_name }}</span>
                            <span class="text-xs font-weight-bold" v-else>—</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="badge badge-sm bg-gradient-success" v-if="item.status=='done'">Done</span>
                            <span class="badge badge-sm bg-gradient-danger" v-else-if="item.status=='cancelled'">Cancelled</span>
                            <span class="badge badge-sm bg-gradient-secondary"  v-else-if="item.status=='abandoned'">Abandoned</span>
                            <span class="badge badge-sm bg-gradient-info"  v-else-if="item.status=='in_progress'">In Progress</span>
                            <span class="badge badge-sm bg-gradient" style="background:var(--bs-orange)"  v-else>Pending</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="badge badge-sm bg-gradient-success" v-if="item.priority=='low'">Low</span>
                            <span class="badge badge-sm bg-gradient-danger" v-else-if="item.priority=='high'">High</span>
                            <span class="badge badge-sm bg-gradient-secondary" style="background:var(--bs-orange)"  v-else-if="item.priority=='mid'">Abandoned</span>
                            <span class="badge badge-sm bg-gradient-secondary" style="background:var(--bs-orange)"  v-else>No Priority</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="text-xs font-weight-bold">{{moment(item.date_created).format("DD MMM, YYYY. hh:mm A") }} </span>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="text-xs font-weight-bold" :class="{'redify':false}"></span>
                          </td>
                        </tr>
                        
                       
                      </tbody>
                    </table>
                    <div class="table-loader" v-if="recentMaintenanceChecklistLoader">
                        <div class="loader"></div>
                    </div>
                  </div>
                </div>
              </div>


              <div class="card my-3" style="" v-if="userData.role=='maintenance_supervisor'">
                <div class="card-header pb-0">
                  <div class="row">
                    <div class="col-lg-6 col-7">
                      <h6 v-if="userData.role=='maintenance_supervisor'">Recent Jobs</h6>
                  
                    </div>
                    <div class="col-lg-6 col-5 my-auto text-end d-none" >
                      <div class="dropdown float-lg-end pe-4">
                        <a class="cursor-pointer" id="dropdownTable" data-bs-toggle="dropdown" aria-expanded="false">
                          <i class="fa fa-ellipsis-v text-secondary"></i>
                        </a>
                        <ul class="dropdown-menu px-2 py-3 ms-sm-n4 ms-n5" aria-labelledby="dropdownTable">
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Action</a></li>
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Another action</a></li>
                          <li><a class="dropdown-item border-radius-md" href="javascript:;">Something else here</a></li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="card-body px-0 pb-2">
                  <div class="table-responsive">
                    <table class="table align-items-center mb-0">
                      <thead>
                        <tr>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Fault Code</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Fault Description</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Truck Number</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Job status</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Job Technician</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Job Duration</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Date Added</th>
                        </tr>
                      </thead>
                      <tbody v-if="jobs && jobs.data.length > 0">
                        <tr v-for="job in jobs.data" :key="job">
                          <td>
                            <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-primary);">
                                {{job.fault_code}}
                            </div>
                          </td>
                          <td class="align-middle text-center t">
                            {{job.description}}
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="text-xs font-weight-bold" > {{job.truck_number}}</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                           
                            <span class="badge badge-sm bg-gradient-info" v-if="job.status=='in_progress'">{{ job.status }}</span>
                            <span class="badge badge-sm bg-gradient-success" v-else-if="job.status=='completed'">{{ job.status }}</span>
                            <span class="badge badge-sm bg-gradient-danger" v-else-if="job.status=='cancelled'">{{ job.status }}</span>
                            <span class="badge badge-sm bg-gradient" style="background:var(--bs-orange)" v-else>{{ job.status }}</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                          
                            <span class="text-xs font-weight-bold" style="text-transform:capitalize">{{job.job_technician.last_name}} {{job.job_technician.first_name}}</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                          
                            <span class="text-xs font-weight-bold" >{{job.expected_job_duration_in_hours}} Hrs</span>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <div class="d-flex px-4 py-1" >
                                <span class="text-xs font-weight-bold" >{{moment(job.job_added).format("DD MMM, YYYY. hh:mm A")}}</span>
                            </div>
                            
                          </td>
                        </tr>
                       
                      </tbody>
                    </table>
                    <div class="table-loader" v-if="recentProjectsLoader">
                        <div class="loader"></div>
                    </div>
                  </div>
                </div>
              </div>


            </div>
            
            <div class="col-lg-4 col-md-6" style="height:fit-content;" v-if="userData.role=='admin' || userData.role == 'maintenance_supervisor'">
              <div class="card h-100">
                <div class="card-header pb-0">
                  <h6>Activities</h6>
                </div>
                <div class="card-body p-3" style="max-height:45rem;overflow-y:auto">
                  <div class="timeline timeline-one-side">

                    <div class="timeline-block mb-3" v-for="activity in activities" :key="activity">
                      <span class="timeline-step">
                        <i class="material-icons text-yellow text-gradient" style="color:var(--bs-yellow);" v-if="activity.status=='pending'">{{activity.icon_tag}}</i>
                        <i class="material-icons text-danger text-gradient" v-else-if="activity.status == 'cancelled'">{{activity.icon_tag}}</i>
                        <i class="material-icons text-success text-gradient" v-else-if="activity.status == 'success'">{{activity.icon_tag}}</i>
                        <i class="material-icons text-info text-gradient" v-else>{{activity.icon_tag}}</i>
                      </span>
                      <div class="timeline-content">
                        <h6 class="text-dark text-sm font-weight-bold mb-0">{{ activity.message }}</h6>
                        <p class="text-secondary font-weight-bold text-xs mt-1 mb-0" v-if="isWithinOneHour(activity.date_added)">{{moment(activity.date_added).fromNow()}} ({{moment(activity.date_added).format("hh:mm A")}})</p>
                        <p class="text-secondary font-weight-bold text-xs mt-1 mb-0" v-else>{{moment(activity.date_added).format("DD MMM, YYYY. hh:mm A")}}</p>
                      </div>
                    </div>

                  
                  </div>
                  <div class="table-loader" v-if="recentActivitiesLoader">
                    <div class="loader"></div>
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

.table-responsive {
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



.redify{
    color:var(--bs-danger)
}

</style>
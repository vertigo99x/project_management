
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
const searchUsersText = ref('');
const recentProjectsLoader = ref(false);
const recentUsersLoader = ref(false);

const status = ref('');
const order = ref('');
const priority = ref('');

const showUsersModal = ref(false);
const confirmDeleteProject = ref(false);
const showCreateProjectModal = ref(false);

const projects = ref(null);
const users = ref(null);

const mode = ref('create');


const projectData = ref({
  id:null,
  project_name:'',
  project_description:'',
  assigned_to:null,
  project_status:'',
  project_priority:'',
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

        const response = await $http.get('api/v1/projects/', {params})
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
                console.error(`Too many requests. try again in a moment`)
                setTimeout(() => {
                    getProjects(page, extraparams);
                }, 1000);
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

async function getUsers(page=null, extraparams=null){
    let params = {}
    recentUsersLoader.value=true;
    try{
        if (page){
        params.page=page;
        }
        if(extraparams){
        params = {...params,...extraparams}
        }

        const response = await $http.get('accounts/users', {params})
        users.value = response.data
        recentUsersLoader.value=false;

    } catch (error){
        recentUsersLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getUsers);
                } else if(status === 429){
                // Too Many Requests, wait for a moment and retry
                console.error(`Too many requests. try again in a moment`)
                setTimeout(() => {
                    getUsers(page, extraparams);
                }, 1000);
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
        //store.commit('setUsercat', userData.value.role)
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

async function submitProject(action='create') {
    
        if(!projectData.value.project_name || !projectData.value.project_description
        || !projectData.value.project_priority
        ){
          toast.error("Fill in the required Fields", {
                  autoClose: 3000,
                  position: toast.POSITION.TOP_RIGHT,
              });
              return ;
        }
        

    try {
      isLoading.value = true;
        const data = {
            "project_name": projectData.value.project_name,
            "project_description": projectData.value.project_description,
            "status": projectData.value.project_status,
            "priority": projectData.value.project_priority.toLowerCase(),
            "assigned_to_id": projectData.value.assigned_to ? projectData.value.assigned_to.id : null
        }

       

        let response = action === 'create' ? await $http.post('api/v1/projects/create/', data) : action === 'update' ? await $http.put(`api/v1/projects/update/${projectData.value.id}/`, data) : action === 'delete' ? await $http.delete(`api/v1/projects/delete/${projectData.value.id}/`) : null
        
        
        toast.info(action === 'delete' ? "Project was Deleted successfully" : response.data.message, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
        //tableLoader=false;
        projectData.value.project_name='';
        projectData.value.project_description='';
        projectData.value.project_status='';
        projectData.value.project_priority='';
        projectData.value.assigned_to=null;
        status.value='';
        order.value='';
        priority.value='';
        searchText.value='';
        confirmDeleteProject.value=false;
        showCreateProjectModal.value=false;
        getProjects();
        isLoading.value = false;
        
    } catch (error) {
      isLoading.value = false;
        if (error.response) {
            const status = error.response.status;
            if (status === 401) {
                // Unauthorized access, attempt to refresh token
                await refreshToken(submitProject(action));
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



const selectProject = (item) => {
  console.log(item)
    projectData.value = {
        id:item.uuid,
        project_name:item.project_name,
        project_description:item.project_description,
        project_priority:item.priority,
        assigned_to:item.assigned_to ? {
          last_name:item.assigned_to.last_name,
          first_name:item.assigned_to.first_name,
        } : null,
        project_status: item.status || '',
        
      }
      mode.value = 'update';
      showCreateProjectModal.value = true;
}

onMounted(() => {
    store.commit('setCurrentPage', 'projects')
    getUserData();
    getProjects();
    
})


</script>


<template>
    <div class="container-fluid py-4" v-if="userData">

        <div class="row">
          <div class="col-12">
            <div class="card my-4">
              <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                <div class="bg-gradient-secondary  border-radius-lg pt-4 pb-3 d-flex align-items-center" style="justify-content: space-between;padding:0 1rem;">
                  <h6 class="text-white text-capitalize ps-3">
                    <span>{{status || "All"}}</span>
                    Projects
                  </h6>
                  <button v-if="userData.role=='admin'" style="background:var(--bs-primary);color:#fff;border:1px solid var(--bs-primary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="projectData={
                    id:null,
                    project_name:'',
                    project_description:'',
                    assigned_to:null,
                    project_status:'',
                    project_priority:'',
                  };mode='create';showCreateProjectModal=true">Create Project+</button>
                </div>
                <div class="searchbar my-3">
                    <input type="text" class="" @keyup.enter="getProjects(null, {status:'', priority:'', order:'', search:searchText});status='';order='';priority='';"  v-model="searchText" placeholder="Search Table" >
                    <button style="background:var(--bs-success);color:#fff;border:1px solid var(--bs-success);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="getProjects(null, {status:'', priority:'', order:'', search:searchText});status='';order='';priority='';">Search</button>
                    <button style="background:var(--bs-secondary);color:#fff;border:1px solid var(--bs-secondary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" class="reset-table" @click="status='';order='';priority='';searchText='';getProjects()">Reset Table</button>
                    
                    
                </div>
                <div class="searchbar my-3">
                    <select name="" id="" v-model="status" @change="getProjects(null, {status, priority, order})">
                        <option value="">All Projects</option>
                        <option value="pending">Pending Projects</option>
                        <option value="done">Done Projects</option>
                        <option value="abandoned">Abandoned Projects</option>
                        <option value="cancelled">Cancelled Projects</option>
                      </select>
                      <select class="mx-2" id="" v-model="priority" @change="getProjects(null, {status, priority, order})">
                        <option value="">All Priorities</option>
                        <option value="low"> Low Priority</option>
                        <option value="mid">Mid Priority</option>
                        <option value="high">High Priority</option>
                       
                      </select>
                      <select class="" id="" v-model="order" @change="getProjects(null, {status, priority, order})">
                        <option value=""> Sort By Oldest</option>
                        <option value="-date_created">Sort By Most Recent</option>
                       
                      </select>
                    
                      
                    
                </div>
              </div>

              <div class="card-body px-0 pb-2">
                <div class="table-responsive p-0">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Project Name</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">project description</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7" v-if="userData.role=='admin'">Assigned to</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">status</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">priority</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">date created</th>

                        <th class="text-secondary opacity-7"></th>
                      </tr>
                    </thead>
                    
                    <tbody v-if="projects">
                      <tr v-for="item in projects.data" :key="item">

                        <td>
                          <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-primary);text-transform: capitalize;">
                              {{item.project_name}}
                          </div>
                        </td>
                        <td class="text-sm">
                          {{item.project_description.length >=30 ? item.project_description.slice(0,30) : item.project_description}}
                        </td>
                        <td class="align-middle text-center text-sm" v-if="userData.role=='admin'">
                          <span class="text-secondary font-weight-bold" v-if="item.assigned_to">{{ item.assigned_to.last_name}} {{ item.assigned_to.first_name }}</span>
                          <span class="text-info font-weight-bold" style="cursor: pointer;" @click="selectProject(item);getUsers();showUsersModal=true;" v-else>Assign User</span>
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
                          <span class="badge badge-sm bg-gradient-secondary" style="background:var(--bs-orange)"  v-else-if="item.priority=='mid'">Mid</span>
                          <span class="badge badge-sm bg-gradient-secondary" style="background:var(--bs-orange)"  v-else>No Priority</span>
                        </td>
                        <td class="align-middle text-center text-sm">
                          <span class="text-xs font-weight-bold">{{moment(item.date_created).format("DD MMM, YYYY. hh:mm A") }} </span>
                        </td>
                        <td class="align-middle text-center text-sm">
                          <span class="text-xs font-weight-bold" :class="{'redify':false}"></span>
                        </td>
                        <td><button style="background:var(--bs-info);color:#fff;border:1px solid var(--bs-info);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="selectProject(item)">View</button>
                        </td>
                      </tr>
                      
                     
                    </tbody>
                  </table>
                  <div class="pagination"  v-if="projects">

                    <div class="controls" v-if="projects.pagination">
                     <span @click="getProjects(null, {status, priority, order, search:searchText, page:projects.pagination.current_page - 1}) "  v-if="projects.pagination.current_page > 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span  v-else-if="projects.pagination.total_pages !== 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span v-for="i in projects.pagination.total_pages" :key="i" @click="getProjects(null, {status, priority, order, search:searchText, page:i}) " :class="{'active':projects.pagination.current_page === i}">
                       {{ i }}
                     </span>
                     <span @click="getProjects(null, {status, priority, order, search:searchText, page:projects.pagination.current_page + 1}) " v-if="projects.pagination.current_page < projects.pagination.total_pages">
                       <i class="material-icons">chevron_right</i>
                     </span>
                    </div>
                 
                     <div class="pagination-info">
                       <span>Page {{ projects.pagination.current_page }} of {{ projects.pagination.total_pages }}</span>
                     </div>
                   </div>
                  <div class="table-loader" v-if="recentProjectsLoader">
                    <div class="loader"></div>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        

        <div class="content-modal" v-if="showCreateProjectModal">
          <div class="modal-content">
            <div class="close-button">
              <span class="svg-icon"
                ><svg
                  @click="showCreateProjectModal = false"
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
            <h3 class="text-secondary mx-2 " style="font-size:24px
            ;margin-top:1rem;text-transform:capitalize;" >{{mode}} Project</h3>
            <div id="reg">
             
              <div class="field2">
                
                <div class="checklist" :class="{'d-flex':userData.role=='user'}">
                  <span>Project Name:</span>
                  <input
                    type="text"
                    id="project_name"
                    v-model="projectData.project_name"
                    v-if="userData.role=='admin'"
                  />
                  <span v-if="userData.role=='user'" class="mx-2 text-dark"> {{projectData.project_name}}</span>
                </div>
                <div class="checklist">
                  <span>Project Description:</span>
                  <textarea  style="resize:none;" name="" id="" cols="30" rows="10" v-model="projectData.project_description" v-if="userData.role=='admin'"></textarea>
                  <p class="text-dark" style="text-overflow: clip;overflow-y:auto;max-height:10rem;" v-else>{{projectData.project_description}}</p>
                </div>
                <div class="checklist d-flex" v-if="userData.role == 'admin'">
                  <span>User:</span>
                  <span class="mx-2 text-info" style="text-transform: capitalize;" v-if="projectData.assigned_to">{{projectData.assigned_to.last_name}} {{projectData.assigned_to.first_name}}</span>
                  <span class="mx-2 text-secondary" style="cursor: pointer;text-decoration: underline;" v-if="projectData.assigned_to" @click="getUsers();showUsersModal=true">Change User?</span>
                  <span class="mx-2 text-info" style="cursor: pointer;text-decoration: underline;" v-else @click="getUsers();showUsersModal=true">Assign User</span>
                </div>
                <div class="px-2">
                  <span>Priority:</span>
                  <select class="mx-2" name="" id="" v-model="projectData.project_priority" v-if="userData.role == 'admin'">
                    <option value="" disabled>Select Priority</option>
                    <option value="low">Low</option>
                    <option value="mid">Mid</option>
                    <option value="high">High</option>
                  </select>
                  <span  class="mx-2 text-dark" v-else>{{ projectData.project_priority }}</span>
                </div>
                <div class="px-2 py-3">
                  <span>Status:</span>
                  <select class="mx-2" name="" id="" v-model="projectData.project_status" v-if="userData.role == 'admin'">
                    <option value="" disabled>Select Status</option>
                    <option value="in_progress" >in_progress</option>
                    <option value="done">done</option>
                    <option value="abandoned">abandoned</option>
                    <option value="cancelled">cancelled</option>
                  </select>
                  <span  class="mx-2 text-dark" v-else>{{ projectData.project_status.replace('_', ' ') }}</span>
                </div>

                <div class="checklist" v-if="userData.role == 'admin'">
                  <span class="text-danger" style="cursor:pointer;text-decoration: underline;" v-if="projectData.project_status!=='cancelled'" @click="projectData.project_status='cancelled';submitProject('update');">Cancel this Project?</span>
                  <span class="text-danger font-weight-bold" style="" v-if="projectData.project_status=='cancelled'">PROJECT WAS CANCELLED</span>
                  <span class="text-info" style="cursor:pointer;text-decoration: underline;" v-if="projectData.project_status=='cancelled'" @click="projectData.project_status='in_progress';submitProject('update');">Revive this Project?</span>
                </div>
                <div class="checklist buttons" v-if="userData.role == 'admin'">
                  <button style="text-transform: capitalize;" v-if="mode == 'create'" @click="submitProject()">Create Project +</button>
                  <button style="text-transform: capitalize;" v-else-if="mode == 'update'" @click="submitProject('update')">Update Project</button>
                  <button  style="text-transform: capitalize;background:var(--bs-danger);" v-if="mode === 'update'" @click="confirmDeleteProject=true">Delete Project</button>
                </div>
               
              </div>
            </div>




          </div>
        </div>


        <div class="content-modal" v-if="showUsersModal">
          <div class="modal-content" style="max-width:55rem;">
            <div class="close-button">
              <span class="svg-icon"
                ><svg
                  @click="showUsersModal = false"
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
            <h3 class="text-dark mx-4" style="margin-bottom:-1rem;font-size:24px
            ;margin-top:1rem;" >Assign A User</h3>
            <div id="reg">
              <div class="searchbar">
                <input type="text" class="mx-4" @keyup.enter="getUsers(null, {search:searchUsersText});"   v-model="searchUsersText" placeholder="Search Users" >
                <button style="background:var(--bs-success);color:#fff;border:1px solid var(--bs-success);margin-left:-10px;border-radius: .5rem;padding:.2rem 1rem;" @click="getUsers(null, {search:searchUsersText});">Search</button>
              
              </div>
              <div class="card-body px-0 pb-2 my-4">
                <div class="table-responsive p-0">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Name</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">email</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">STATUS</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Date Joined</th>
              
                        <th class="text-secondary opacity-7"></th>
                      </tr>
                    </thead>
                    
                    <tbody v-if="users">
                      <tr v-for="item in users.data" :key="item">

                        <td style="cursor: pointer;" @click="projectData.assigned_to = {id:item.id,last_name:item.last_name,first_name:item.first_name};showUsersModal=false">
                          <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-primary);text-transform: capitalize;">
                              {{item.last_name}} {{item.first_name}}
                          </div>
                        </td>
                        <td class="text-sm">
                          {{item.email}}
                        </td>
                        
                        <td class="align-middle text-center text-sm">
                          <span class="badge badge-sm bg-gradient-success" v-if="item.is_active">Active</span>
                          <span class="badge badge-sm bg-gradient-secondary" v-else>Inactive</span>
                        </td>
                      
                        <td class="align-middle text-center text-sm">
                          <span class="text-xs font-weight-bold">{{moment(item.date_created).format("DD MMM, YYYY. hh:mm A") }} </span>
                        </td>
                        
                        <td class="align-middle text-center">
                          <span style="background:var(--bs-info);color:#fff;border:1px solid var(--bs-info);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="projectData.assigned_to = {id:item.id,last_name:item.last_name,first_name:item.first_name};showUsersModal=false">Assign User</span>
                        </td>
                      </tr>
                      
                     
                    </tbody>
                  </table>
                  
                  <div class="table-loader" v-if="recentProjectsLoader">
                    <div class="loader"></div>
                </div>
                
                </div>
                <div class="pagination"  v-if="projects">

                  <div class="controls" v-if="projects.pagination">
                   <span @click="getProjects(null, {status, priority, order, search:searchText, page:projects.pagination.current_page - 1}) "  v-if="projects.pagination.current_page > 1">
                     <i class="material-icons">chevron_left</i>
                   </span>
                   <span  v-else-if="projects.pagination.total_pages !== 1">
                     <i class="material-icons">chevron_left</i>
                   </span>
                   <span v-for="i in projects.pagination.total_pages" :key="i" @click="getProjects(null, {status, priority, order, search:searchText, page:i}) " :class="{'active':projects.pagination.current_page === i}">
                     {{ i }}
                   </span>
                   <span @click="getProjects(null, {status, priority, order, search:searchText, page:projects.pagination.current_page + 1}) " v-if="projects.pagination.current_page < projects.pagination.total_pages">
                     <i class="material-icons">chevron_right</i>
                   </span>
                  </div>
               
                   <div class="pagination-info">
                     <span>Page {{ projects.pagination.current_page }} of {{ projects.pagination.total_pages }}</span>
                   </div>
                 </div>
              </div>
            </div>




          </div>
        </div>


       
          
          <div class="content-modal" v-if="confirmDeleteProject">
            <div class="modal-content">
              <h2>Confirm Delete Project?</h2>
              <p>Are you sure you want to delete this Project?</p>
              <div class="buttonbox" style="display: flex;justify-content: space-between;">
                <button @click="confirmDeleteProject=false;" style="background-color: var(--bs-info);">Cancel</button>
                <button @click="submitProject('delete')" class="bg-danger" style="">Delete</button>
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
  

  .checklist.buttons{
    display: flex;
    flex-direction:row-reverse;
    justify-content: space-between;
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
  .checklist.buttons{
    display: flex;
    flex-direction:column;
    justify-content:flex-start;

    button:last-child{
      margin-top:1rem;
    }
  }
    .searchbar{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      input{
        width:100%;
      }
      
      button{
        margin-top:1rem;
        margin-left:-1rem;
      }
      
    }

    .searchbar:nth-child(3){
        display:flex;
        flex-direction: row;

        select{
            width:100%;
            margin:.5rem 0 !important;
            padding:.2rem;

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
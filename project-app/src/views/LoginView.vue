<script setup>
import { ref, reactive, inject, onMounted } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const $http = inject('$http');
const router = useRouter();
const route = useRoute(); // Use useRoute to get current route
const store = useStore();

const current_state = ref('login')

const login = ref({
    username: '',
    password: '',
});

const register = ref({
    username: '',
    password: '',
    confirm_password: '',
    user:'',
    first_name:'',
    last_name:'',
});

const login_error = ref(null);
const isLoading = ref(false);

const redirectBots = () => {
    // flag IP address and redirect;
};


onMounted(() => {
    store.commit('resetStore')
});

function validatePassword(password) {
  //const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return password.length >= 8; //passwordRegex.test(password);
}

async function submitLogin() {
    const username = login.value.username.trim();
    const password = login.value.password;

    if (!username || !password) {
        toast.error('Please complete all fields', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });
        return;
    }

    const formData = {
        email: username,
        password: password,
    };

    try {
        isLoading.value = true;
        const response = await $http.post('api/token', formData);
        const { access, refresh } = response.data;

        store.commit('setRefresh', refresh);
        store.commit('setAccess', access);

        $http.defaults.headers.common['Authorization'] = `Bearer ${access}`; // Setting the header globally

        // Success notification
        toast.success('Logged in Successfully', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });

        // Handle redirection
        const redirectPath = route.query.redirect || '/'; // Access query param from the route
        router.push(redirectPath);
    } catch (error) {
        console.error(error);
        isLoading.value = false;

        if (error.response) {
            const errorMessages = Object.values(error.response.data);
            login_error.value = errorMessages[0] || 'An error occurred';

            toast.error(login_error.value, {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        } else {
            toast.error('An unexpected error occurred', {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        }
    } finally {
        isLoading.value = false;
    }
}

async function submitRegister() {
    const username = register.value.username.trim();
    const password = register.value.password;
    const confirm_password = register.value.confirm_password;
    const user = register.value.user;
    const first_name = register.value.first_name;
    const last_name = register.value.last_name;

    if (!username || !password || !user || !confirm_password || !first_name || !last_name) {
        toast.error('Please complete all fields', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });
        return;
    }

    else if(password !== confirm_password) {
       toast.error('Passwords do not match', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });
        return;
    } else if (!validatePassword(password)) {
       toast.error('Password must be at least 8 characters long', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });
        return;
    }

    const formData = {
        first_name: first_name,
        last_name: last_name,
        email: username,
        password: password,
        role: user,
    };

    try {
        isLoading.value = true;
        const response = await $http.post('accounts/create-user/', formData);
        const { access, refresh } = response.data;

        
        toast.success('Registered Successfully', {
            autoClose: 3000,
            position: toast.POSITION.TOP_RIGHT,
        });

        current_state.value = 'login';
        login.value = {
            username: '',
            password: '',
        }
        register.value = {
          username: '',
          password: '',
          confirm_password: '',
          user:'',
          first_name:'',
          last_name:'',
        }
    } catch (error) {
        console.error(error);
        isLoading.value = false;

        if (error.response) {
            const errorMessages = Object.values(error.response.data);
            login_error.value = errorMessages[0] || 'An error occurred';

            toast.error(login_error.value, {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        } else {
            toast.error('An unexpected error occurred', {
                autoClose: 3000,
                position: toast.POSITION.TOP_RIGHT,
            });
        }
    } finally {
        isLoading.value = false;
    }
}
</script>



<template>
    <main class="main-content  mt-0">
        <div class="honeypot">
            <form id="loginForm" @submit="redirectBots">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
          
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
          
                <!-- Honeypot Field (hidden from legitimate users) -->
                <input type="text" id="honeypot" name="honeypot" class="honeypot-field" autocomplete="off">
          
                <button type="submit" @click="redirectBots">Login</button>
              </form>
        </div>


        <div class="page-header min-vh-100">
            <div class="container">
              <div class="row">
                <div class="col-6 d-lg-flex d-none h-100 my-auto pe-0 position-absolute top-0 start-0 text-center justify-content-center flex-column">
                  <div class="position-relative bg-gradient-primary h-100 m-3 px-7 border-radius-lg d-flex flex-column justify-content-center" style="background-image: url('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'); background-size: cover;z-index:999">
                  </div>
                </div>
                <div class="col-xl-4 col-lg-5 col-md-7 d-flex flex-column ms-auto me-auto ms-lg-auto me-lg-5 main-body" v-if="current_state=='login'">
                  <div class="card card-plain" id="formcard">
                    <div class="card-header" style="background-color: var(--bs-primary);">
                      <h4 class="font-weight-bolder text-center" style="color:#fff;">Sign In</h4>
                      <p class="mb-0"></p>
                    </div>
                    <div class="card-body" >
                      <form role="form" @keyup.enter="submitLogin" require="true">
                       
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="email" class="form-control" v-model="login.username" placeholder="Email Address">
                        </div>
                        
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="password" class="form-control" v-model="login.password" placeholder="Password">
                        </div>
                        
                        <div class="text-center">
                          <button type="button" class="btn btn-lg bg-gradient-secondary btn-lg w-100 mt-4 mb-0" @click="submitLogin()" :disabled="!login.password || !login.username">Sign In</button>
                        </div>

                        <div class="text-dark mt-4">
                          <p>New User? <span class="text-primary font-weight-bold" style="cursor:pointer;" @click="current_state='register'">Register</span></p>
                        </div>

                        
                      </form>
                    </div>

                   
                  </div>
                </div>
                <div class="col-xl-4 col-lg-5 col-md-7 d-flex flex-column ms-auto me-auto ms-lg-auto me-lg-5 main-body" v-if="current_state=='register'">
                  <div class="card card-plain" id="formcard">
                    <div class="card-header" style="background-color: var(--bs-primary);">
                      <h4 class="font-weight-bolder text-center" style="color:#fff;">Sign Up </h4>
                      <p class="mb-0"></p>
                    </div>
                    <div class="card-body" >
                      <form role="form" @keyup.enter="submitRegister">
                       
                        <div class="input-group input-group-outline mb-3">
                          
                          <select name="" id="" class="form-control" v-model="register.user">
                            <option value="" selected disabled>Select User Category</option>
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                          </select>
                        </div>
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="email" class="form-control" v-model="register.username" placeholder="Email Address">
                        </div>
                        <div class="input-group input-group-outline mb-3" style="gap:1rem;">
                          
                          <input type="text" class="form-control" v-model="register.first_name" placeholder="First Name">
                          <input type="text" class="form-control" v-model="register.last_name" placeholder="Last Name">
                        </div>
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="password" class="form-control" v-model="register.password"  style="font-size:16px" :class="{'bg-err':!validatePassword(register.password) && register.password.length > 0}" placeholder="Password">
                        </div>
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="password" class="form-control" v-model="register.confirm_password" style="font-size:16px"  :class="{'bg-err':register.password !== register.confirm_password && register.confirm_password.length > 1}"  placeholder="Confirm Password">
                        </div>
                        
                        <div class="text-center">
                          <button type="button" class="btn btn-lg bg-gradient-secondary btn-lg w-100 mt-4 mb-0" @click="submitRegister()" :disabled="!validatePassword(register.password) || register.password !== register.confirm_password || !register.first_name || !register.last_name || !register.user || !register.username">Sign Up</button>
                        </div>

                        <div class="text-dark mt-4">
                          <p>Already a User? <span class="text-primary font-weight-bold" style="cursor:pointer;" @click="current_state='login'">Login</span></p>
                        </div>

                        
                      </form>
                    </div>

                   
                  </div>
                </div>
              </div>
            </div>
          </div>
        <div class="loading" v-if="isLoading">
            <div class="loader"></div>
        </div>
      </main>
</template>

<style scoped lang="scss">
.honeypot{
    display: none;
}

#formcard{
    box-shadow:12px 12px 12px rgba(0,0,0,0.1), 
    -10px -10px 10px var(--bs-white);
}

.dark-version #formcard{
    box-shadow:none;
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
        animation: spin 2s linear infinite;
    }
}

.main-body{
  animation: shake .3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  
  .card-body{
    animation: fadein .5s ease-in-out forwards;
    opacity: 0;
    
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
@keyframes shake {
  0%{
    transform: translateX(0%)
  }
  25%{
    transform: translateX(-25%)
  }
  25%{
    transform: translateX(25%)
  }
  100%{
    
  }  
}

.bg-err{
  background: rgba(255,0,0,0.3) !important;
}

input::placeholder{
  color:var(--bs-dark);
}

</style>
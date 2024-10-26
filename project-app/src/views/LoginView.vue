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

const login = reactive({
    username: '',
    password: '',
});

const login_error = ref(null);
const isLoading = ref(false);

const redirectBots = () => {
    // flag IP address and redirect;
};


onMounted(() => {
    store.commit('resetStore')
});

async function submitLogin() {
    const username = login.username.trim();
    const password = login.password;

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
                  <div class="position-relative bg-gradient-primary h-100 m-3 px-7 border-radius-lg d-flex flex-column justify-content-center" style="background-image: url('https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'); background-size: cover;">
                  </div>
                </div>
                <div class="col-xl-4 col-lg-5 col-md-7 d-flex flex-column ms-auto me-auto ms-lg-auto me-lg-5">
                  <div class="card card-plain" id="formcard">
                    <div class="card-header" style="background-color: var(--bs-primary);">
                      <h4 class="font-weight-bolder text-center" style="color:#fff;">Sign In</h4>
                      <p class="mb-0"></p>
                    </div>
                    <div class="card-body" >
                      <form role="form" @keyup.enter="submitLogin">
                       
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="email" class="form-control" v-model="login.username" placeholder="Username">
                        </div>
                        <div class="input-group input-group-outline mb-3">
                          
                          <input type="password" class="form-control" v-model="login.password" placeholder="Password">
                        </div>
                        
                        <div class="text-center">
                          <button type="button" class="btn btn-lg bg-gradient-secondary btn-lg w-100 mt-4 mb-0" @click="submitLogin()">Sign In</button>
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

@keyframes spin {
    100%{
        transform: rotate(360deg);
    }
}

</style>
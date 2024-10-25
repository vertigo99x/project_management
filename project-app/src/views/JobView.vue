
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
const searchTechnicianText = ref('');
const recentJobsLoader = ref(false);
const recentTechniciansLoader = ref(false);
const selectTechnicianModal = ref(false);
const confirmCancelJobModal = ref(false);
const showCreateJobModal = ref(false);
const selectedJob = ref(null);

const status = ref('pending');
const order = ref('');


const jobs = ref(null);
const technicians = ref(null);
const selectedTruck = ref(null);
const selectedFault = ref(null);
const selectedTechnician = ref(null);
const selectedJobTruckNumber = ref('');

const fault_description = ref('');








const fault_list = ref([
    {"Fault_Area_Code": "DIAG", "Symptom_Code": "DIABS01", "Code": "DIAG016", "Description": "Brake System Fault", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIACF01", "Code": "DIAG007", "Description": "Clutch Fault", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIACG01", "Code": "DIAG005", "Description": "Cutting of gas", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAEU01", "Code": "DIAG018", "Description": "Electronic Unit Pump", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAGGL001", "Code": "DIAG101", "Description": "Gas Leakage", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAHR01", "Code": "DIAG012", "Description": "Head/Rear Light Fault", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAHS01", "Code": "DIAG006", "Description": "Hard Starting Fault", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAIS01", "Code": "DIAG014", "Description": "Ignition System Fault", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIALK01", "Code": "DIAG001", "Description": "Oil leakage", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIALK02", "Code": "DIAG002", "Description": "Air leakage", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIALK03", "Code": "DIAG003", "Description": "Water Leakage", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAPF01", "Code": "DIAG015", "Description": "Propeller Fault", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIASF01", "Code": "DIAG020", "Description": "Shock Absorber Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIASF02", "Code": "DIAG021", "Description": "Cab Barrel Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIASF03", "Code": "DIAG022", "Description": "Cab Bushing Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIASF04", "Code": "DIAG023", "Description": "Cab Jack Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIASS01", "Code": "DIAG019", "Description": "Steering System Fault", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIATF01", "Code": "DIAG010", "Description": "Transmission Fault", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAWH01", "Code": "DIAG013", "Description": "Wheel Drum/Hub Fault", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "DIAG", "Symptom_Code": "DIAWS01", "Code": "DIAG017", "Description": "Wiper Stick replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAH01", "Code": "ELEC022", "Description": "Air Horn Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAH02", "Code": "ELEC023", "Description": "Air Horn Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAH03", "Code": "ELEC024", "Description": "Air Horn Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAH04", "Code": "ELEC025", "Description": "Air Horn Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAL01", "Code": "ELEC030", "Description": "Alternator Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAL02", "Code": "ELEC031", "Description": "Alternator Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAL03", "Code": "ELEC032", "Description": "Alternator Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELAL04", "Code": "ELEC033", "Description": "Alternator Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELBA01", "Code": "ELEC026", "Description": "Battery Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELBA02", "Code": "ELEC027", "Description": "Battery Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELBA03", "Code": "ELEC028", "Description": "Battery Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELBA04", "Code": "ELEC029", "Description": "Battery Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELBR001", "Code": "ELEC038", "Description": "Bulb Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELEC01", "Code": "ELEC017", "Description": "Electronic Control Module Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELEC02", "Code": "ELEC018", "Description": "Electronic Control Module Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELEC03", "Code": "ELEC019", "Description": "Electronic Control Module Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELEC04", "Code": "ELEC020", "Description": "Electronic Control Module Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELEC05", "Code": "ELEC021", "Description": "Electronic Control Module Configuration", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELECDR000", "Code": "ELEC039", "Description": "Dashboard Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELECDR500", "Code": "ELEC040", "Description": "Dashboard Replacement", "Expected_Duration_Hrs": 3.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELHL001", "Code": "ELEC042", "Description": "High and Low Gear Cover Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELHL01", "Code": "ELEC005", "Description": "Head Lamp Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELHL02", "Code": "ELEC006", "Description": "Head Lamp Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELHL03", "Code": "ELEC007", "Description": "Head Lamp Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELHL04", "Code": "ELEC008", "Description": "Head Lamp Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELIC01", "Code": "ELEC013", "Description": "Instrument Cluster Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELIC02", "Code": "ELEC014", "Description": "Instrument Cluster Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELIC03", "Code": "ELEC015", "Description": "Instrument Cluster Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELIC04", "Code": "ELEC016", "Description": "Instrument Cluster Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELKS01", "Code": "ELEC034", "Description": "Kick Starter Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELKS02", "Code": "ELEC035", "Description": "Kick Starter Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELKS03", "Code": "ELEC036", "Description": "Kick Starter Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELKS04", "Code": "ELEC037", "Description": "Kick Starter Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRA01", "Code": "ELEC009", "Description": "Reverse Alarm Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRA02", "Code": "ELEC010", "Description": "Reverse Alarm Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRA04", "Code": "ELEC012", "Description": "Reverse Alarm Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRL01", "Code": "ELEC001", "Description": "Rear Light Replacement", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRL03", "Code": "ELEC042", "Description": "Gear selector Cable repair", "Expected_Duration_Hrs": 3.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRL04", "Code": "ELEC004", "Description": "Rear Light Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELRL04", "Code": "ELEC041", "Description": "Connecting Wire Replacement", "Expected_Duration_Hrs": 1.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "ELEC", "Symptom_Code": "ELWB001", "Code": "ELEC041", "Description": "Wiper Blade Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABBO01", "Code": "FABR062", "Description": "Burning of Bolts", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABBR001", "Code": "FABR077", "Description": "Bumper Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABBR002", "Code": "FABR078", "Description": "Bumper Repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABCL01", "Code": "FABR063", "Description": "Cabin Leak Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABCT01", "Code": "FABR066", "Description": "Cabin Trim Repairs", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABCT02", "Code": "FABR067", "Description": "Cabin Trim Replacement", "Expected_Duration_Hrs": 10, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABCT02", "Code": "FABR074", "Description": "Cab Jack Repairs", "Expected_Duration_Hrs": 1.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDB01", "Code": "FABR036", "Description": "Dashboard Removal", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDB02", "Code": "FABR037", "Description": "Dashboard Installation", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH01", "Code": "FABR058", "Description": "Door Hinge Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH02", "Code": "FABR059", "Description": "Door Hinge Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH03", "Code": "FABR060", "Description": "Door Hinge Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH04", "Code": "FABR061", "Description": "Door Hinge Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH04", "Code": "FABR073", "Description": "Bonnet Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDH05", "Code": "FABR074", "Description": "Bonnet Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDL01", "Code": "FABR054", "Description": "Door Lock Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDL02", "Code": "FABR055", "Description": "Door Lock Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDL03", "Code": "FABR056", "Description": "Door Lock Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABDL04", "Code": "FABR057", "Description": "Door Lock Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABEP02", "Code": "FABR018", "Description": "Exhaust Pot Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABEP03", "Code": "FABR019", "Description": "Exhaust Pot Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABEP04", "Code": "FABR020", "Description": "Exhaust Pot Repair", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFF01", "Code": "FABR001", "Description": "Front Fender Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFF02", "Code": "FABR002", "Description": "Front Fender Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFF04", "Code": "FABR004", "Description": "Front Fender Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFT01", "Code": "FABR013", "Description": "Fuel Tank Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFT02", "Code": "FABR014", "Description": "Fuel Tank Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFT03", "Code": "FABR015", "Description": "Fuel Tank Replacement", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFT04", "Code": "FABR016", "Description": "Fuel Tank Repair", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFW01", "Code": "FABR021", "Description": "Fifth Wheel Repair", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFW02", "Code": "FABR022", "Description": "Fifth Wheel Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFW03", "Code": "FABR023", "Description": "Fifth Wheel Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABFW04", "Code": "FABR024", "Description": "Fifth Wheel Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABIN01", "Code": "FABR045", "Description": "Intercooler Repairs", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABMG01", "Code": "FABR009", "Description": "Mud Guard Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABMG02", "Code": "FABR010", "Description": "Mud Guard Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABMG03", "Code": "FABR011", "Description": "Mud Guard Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABMG04", "Code": "FABR012", "Description": "Mud Guard Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABRAD01", "Code": "FABR044", "Description": "Radiator Repairs", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABRTR500", "Code": "FABR072", "Description": "Tarpaulin Repairs", "Expected_Duration_Hrs": 2.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSB01", "Code": "FABR040", "Description": "Seat Belt Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSB02", "Code": "FABR041", "Description": "Seat Belt Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSB03", "Code": "FABR042", "Description": "Seat Belt Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE01", "Code": "FABR005", "Description": "Step Entrance Box Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE01", "Code": "FABR068", "Description": "Seat Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE01", "Code": "FABR075", "Description": "Sand Protector Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE02", "Code": "FABR006", "Description": "Step Entrance Box Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE02", "Code": "FABR069", "Description": "Seat Replacement", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE03", "Code": "FABR070", "Description": "Seat Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE04", "Code": "FABR008", "Description": "Step Entrance Box Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSE04", "Code": "FABR071", "Description": "Seat Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSM01", "Code": "FABR028", "Description": "Side Mirror Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSM02", "Code": "FABR029", "Description": "Side Mirror Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSM03", "Code": "FABR030", "Description": "Side Mirror Installation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSM04", "Code": "FABR031", "Description": "Side Mirror Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSU01", "Code": "FABR064", "Description": "Seat Uphosltery Repairs", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABSU02", "Code": "FABR065", "Description": "Seat Uphosltery Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWG01", "Code": "FABR046", "Description": "Window Glass Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWG02", "Code": "FABR047", "Description": "Window Glass Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWG03", "Code": "FABR048", "Description": "Window Glass Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWG04", "Code": "FABR049", "Description": "Window Glass Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWL01", "Code": "FABR050", "Description": "Window Lifter Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWL02", "Code": "FABR051", "Description": "Window Lifter Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWL03", "Code": "FABR052", "Description": "Window Lifter Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWL04", "Code": "FABR053", "Description": "Window Lifter Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWM01", "Code": "FABR032", "Description": "Wiper Motor Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWM02", "Code": "FABR033", "Description": "Wiper Motor Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWM03", "Code": "FABR034", "Description": "Wiper Motor Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWM04", "Code": "FABR035", "Description": "Wiper Motor Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWS01", "Code": "FABR025", "Description": "Windscreen Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWS02", "Code": "FABR026", "Description": "Windscreen Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "FABWS03", "Code": "FABR027", "Description": "Windscreen Replacement", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "MECSB001", "Code": "FABR074", "Description": "Stabilizer Bushing Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "MECSP001", "Code": "FAB076", "Description": "Complete Spring Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "FABR", "Symptom_Code": "MECTSB001", "Code": "FABR075", "Description": "Tunnel Seating (41mm) Bolt Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "LUB", "Symptom_Code": "LUB001", "Code": "LUB003", "Description": "Lubrication", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "LUB", "Symptom_Code": "LUBDO001", "Code": "LUB002", "Description": "Differential Oil Refill", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "LUB", "Symptom_Code": "LUBGO001", "Code": "LUB001", "Description": "Gear Oil Inspection And Refill", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "DIAHS01", "Code": "MECH99", "Description": "Replacement of Cabin filter", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX01", "Code": "MECH038", "Description": "Axle Removal", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX01", "Code": "MECH064", "Description": "Axle Tunnel Removal", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX02", "Code": "MECH039", "Description": "Axle Installation", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX02", "Code": "MECH065", "Description": "Axle Tunnel Installation", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX03", "Code": "MECH040", "Description": "Axle Replacement", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX03", "Code": "MECH066", "Description": "Axle Tunnel Replacement", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX04", "Code": "MECH067", "Description": "Axle Tunnel Repairs", "Expected_Duration_Hrs": 10, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX05", "Code": "MECH068", "Description": "Axle Seating Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX06", "Code": "MECH069", "Description": "Axle Seating Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX07", "Code": "MECH070", "Description": "Axle Seating Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX08", "Code": "MECH071", "Description": "Axle Seating Repairs", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX09", "Code": "MECH081", "Description": "Axle Pinion Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX10", "Code": "MECH082", "Description": "Axle Pinion Installation", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX11", "Code": "MECH083", "Description": "Axle Pinion Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECAX12", "Code": "MECH084", "Description": "Axle Pinion Repair", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBJ01", "Code": "MECH008", "Description": "Ball Joint Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBJ02", "Code": "MECH009", "Description": "Ball Joint Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBJ03", "Code": "MECH010", "Description": "Ball Joint Replacement", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR01", "Code": "MECH029", "Description": "Brake Lining Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR02", "Code": "MECH030", "Description": "Brake Lining Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR03", "Code": "MECH031", "Description": "Brake Lining Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR04", "Code": "MECH032", "Description": "Brake Pad Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR04", "Code": "MECH103", "Description": "Brake Calliper Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR05", "Code": "MECH033", "Description": "Brake Pad Installation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR06", "Code": "MECH034", "Description": "Brake Pad Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR07", "Code": "MECH119", "Description": "Brake Air Line Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR08", "Code": "MECH120", "Description": "Brake Air Line Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR09", "Code": "MECH121", "Description": "Brake Air Line Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECBR10", "Code": "MECH122", "Description": "Brake Air Line Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCB01", "Code": "MECH090", "Description": "Centre Bolt Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCB02", "Code": "MECH091", "Description": "Centre Bolt Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCB03", "Code": "MECH092", "Description": "Centre Bolt Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCH01", "Code": "MECH035", "Description": "Cylinder Head Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCH02", "Code": "MECH036", "Description": "Cylinder Head Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCH03", "Code": "MECH037", "Description": "Cylinder Head Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL01", "Code": "MECH054", "Description": "Clutch Disc Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL02", "Code": "MECH055", "Description": "Clutch Disc Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL03", "Code": "MECH056", "Description": "Clutch Disc Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL04", "Code": "MECH057", "Description": "Clutch Plate Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL05", "Code": "MECH058", "Description": "Clutch Plate Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL06", "Code": "MECH059", "Description": "Clutch Plate Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL07", "Code": "MECH136", "Description": "Upper clutch replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL08", "Code": "MECH137", "Description": "Clutch booster Replacement", "Expected_Duration_Hrs": 0.4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCL09", "Code": "MECH138", "Description": "Clutch booster Repair", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCO01", "Code": "MECH134", "Description": "Air Compressor Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECCO02", "Code": "MECH135", "Description": "Air Compressor Repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECDB01", "Code": "MECH085", "Description": "Damper Rubber Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEN01", "Code": "MECH001", "Description": "Engine Troubleshooting", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEN01", "Code": "MECH160", "Description": "Overheating", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEN02", "Code": "MECH002", "Description": "Engine Overhaul", "Expected_Duration_Hrs": 21, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEN03", "Code": "MECH003", "Description": "Engine Installation", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEN04", "Code": "MECH004", "Description": "Engine Replacement", "Expected_Duration_Hrs": 14, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEQ02", "Code": "MECH096", "Description": "Equalizer Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEQ03", "Code": "MECH097", "Description": "Equalizer Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEQ04", "Code": "MECH098", "Description": "Equalizer Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEQ05", "Code": "MECH099", "Description": "Equalizer Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEU01", "Code": "MECH111", "Description": "Electronic Unit Pump Repairs", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEU02", "Code": "MECH112", "Description": "Electronic Unit Pump Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEU03", "Code": "MECH113", "Description": "Electronit Unit Pump Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECEU04", "Code": "MECH114", "Description": "Electronic Unit Pump Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFB01", "Code": "MECH051", "Description": "Fan Belt replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFB02", "Code": "MECH052", "Description": "Fan Belt Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFB03", "Code": "MECH053", "Description": "Fan Belt Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFG01", "Code": "MECH107", "Description": "Fuel Guage Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFG02", "Code": "MECH108", "Description": "Fuel Guage Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFG03", "Code": "MECH109", "Description": "Fuel Guage Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECFG04", "Code": "MECH110", "Description": "Fuel Guage Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHBW001", "Code": "MECH138", "Description": "Brake Adjustment", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHBW002", "Code": "MECH139", "Description": "Brake Adjuster Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHFK001", "Code": "MECH140", "Description": "Front King Pin Repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHFR001", "Code": "MECH143", "Description": "Flywheel Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHFR301", "Code": "MECH140", "Description": "Fuel Rail Sensor Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHPL301", "Code": "MECH142", "Description": "Pressure Limiter Valve Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHTK001", "Code": "MECH141", "Description": "Turntable King Pin Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHVT301", "Code": "MECH141", "Description": "Vehicle Tool Kit Collection", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECHWR301", "Code": "MECH144", "Description": "Water Seperator Replacement (NX)", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIC01", "Code": "MECH126", "Description": "Intercooler Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIC02", "Code": "MECH127", "Description": "Intercooler Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIC03", "Code": "MECH128", "Description": "Intercooler Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIN01", "Code": "MECH014", "Description": "Injector Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIN02", "Code": "MECH015", "Description": "Injector Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIN03", "Code": "MECH016", "Description": "Injector Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECIN04", "Code": "MECH017", "Description": "Injector Overhauling", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECKP001", "Code": "MECH139", "Description": "Front King Pin Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO01", "Code": "MECH018", "Description": "Nozzle Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO02", "Code": "MECH019", "Description": "Nozzle Installation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO03", "Code": "MECH020", "Description": "Nozzle Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO04", "Code": "MECH021", "Description": "Nozzle Overhauling", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO05", "Code": "MECH022", "Description": "Nozzle Pipe Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO06", "Code": "MECH023", "Description": "Nozzle Pipe Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO07", "Code": "MECH024", "Description": "Nozzle Pipe Installation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO08", "Code": "MECH025", "Description": "Nozzle Pipe Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECNO08", "Code": "MECH139", "Description": "Timing Washer", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECPR01", "Code": "MECH047", "Description": "Propeller Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECPR02", "Code": "MECH048", "Description": "Propeller Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECPR03", "Code": "MECH049", "Description": "Propeller Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECPR04", "Code": "MECH050", "Description": "Propeller Repairs", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECRA01", "Code": "MECH123", "Description": "Radiator Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECRA03", "Code": "MECH125", "Description": "Radiator Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECRE01", "Code": "MECH044", "Description": "Routine Engine Interval Service", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB01", "Code": "MECH100", "Description": "Spider Bearing Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB02", "Code": "MECH101", "Description": "Spider Bearing Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB03", "Code": "MECH102", "Description": "Spider Bearing Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB05", "Code": "MECH104", "Description": "Brake Calliper Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB06", "Code": "MECH105", "Description": "Brake Calliper Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSB07", "Code": "MECH106", "Description": "Brake Calliper Repair", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP01", "Code": "MECH011", "Description": "Steering Pump Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP01", "Code": "MECH041", "Description": "Trailer Spring Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP02", "Code": "MECH012", "Description": "Steering Pump Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP02", "Code": "MECH042", "Description": "Trailer Spring Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP02", "Code": "MECH093", "Description": "Shackle Pin Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP03", "Code": "MECH013", "Description": "Steering Pump Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP03", "Code": "MECH043", "Description": "Spring Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP03", "Code": "MECH094", "Description": "Shackle Pin Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP04", "Code": "MECH044", "Description": "Tractor Spring Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP04", "Code": "MECH095", "Description": "Shackle Pin Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP06", "Code": "MECH043", "Description": "Front Spring Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECSP07", "Code": "MECH044", "Description": "Front Spring Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTA01", "Code": "MECH045", "Description": "Tractor Axle Service", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTA01", "Code": "MECH046", "Description": "Trailer Axle Service", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTH02", "Code": "MECH130", "Description": "Throttle Cable Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTR01", "Code": "MECH131", "Description": "Tie Rod Ends Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTR03", "Code": "MECH133", "Description": "Tie rod rubber replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTR04", "Code": "MECH134", "Description": " Complete Tie rod replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTU01", "Code": "MECH005", "Description": "Turbo charger Installation", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTU02", "Code": "MECH006", "Description": "Turbo charger Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECTU03", "Code": "MECH007", "Description": "Turbo charger Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECUC01", "Code": "MECH086", "Description": "U-Clip Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECUC02", "Code": "MECH087", "Description": "U-Clip Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECUC03", "Code": "MECH088", "Description": "U-Clip Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECUC04", "Code": "MECH089", "Description": "U-Clip Repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECVB01", "Code": "MECH115", "Description": "V-bar Removal", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECVB02", "Code": "MECH116", "Description": "V-bar Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECVB03", "Code": "MECH117", "Description": "V-bar Replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECVB04", "Code": "MECH118", "Description": "V-bar Repairs", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH01", "Code": "MECH060", "Description": "Wheel Bearing Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH02", "Code": "MECH061", "Description": "Wheel Bearing Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH03", "Code": "MECH062", "Description": "Wheel Bearing Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH04", "Code": "MECH063", "Description": "Trailer Wheel Alignment", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH05", "Code": "MECH072", "Description": "Wheel Brake Disc Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH06", "Code": "MECH073", "Description": "Wheel Brake Disc Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH07", "Code": "MECH074", "Description": "Wheel Brake Disc Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH08", "Code": "MECH075", "Description": "Wheel Drum Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH09", "Code": "MECH076", "Description": "Wheel Drum Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH10", "Code": "MECH077", "Description": "Wheel Drum Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH11", "Code": "MECH078", "Description": "Wheel Hub Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH12", "Code": "MECH079", "Description": "Wheel Hub Installation", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWH13", "Code": "MECH080", "Description": "Wheel Hub Replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWS01", "Code": "MECH026", "Description": "Wheel Stud Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWS02", "Code": "MECH027", "Description": "Wheel Stud Installation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "MECH", "Symptom_Code": "MECWS03", "Code": "MECH028", "Description": "Wheel Stud Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT01", "Code": "PAIN001", "Description": "Partial Cabin Spray Painting", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT02", "Code": "PAIN002", "Description": "Whole Cabin Spray Painting", "Expected_Duration_Hrs": 14, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT03", "Code": "PAIN003", "Description": "Partial Semi Trailer Spray Painting", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT04", "Code": "PAIN004", "Description": "Whole Semi Trailer Spray Painting", "Expected_Duration_Hrs": 14, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT05", "Code": "PAIN005", "Description": "Partial Box Body Spray Painting", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT06", "Code": "PAIN006", "Description": "Whole Box Body Spray Painting", "Expected_Duration_Hrs": 14, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT07", "Code": "PAIN007", "Description": "Door Spray Painting", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT08", "Code": "PAIN008", "Description": "Rim Spray Painting", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PAIN", "Symptom_Code": "PAINT09", "Code": "PAIN009", "Description": "Bumper Spray Painting", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "DIALK02", "Code": "DIAN3", "Description": "Complete Air drier Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAH01", "Code": "PNEU013", "Description": "Air Hose Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAH02", "Code": "PNEU014", "Description": "Air Hose Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAH03", "Code": "PNEU015", "Description": "Air Hose Removal", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAH04", "Code": "PNEU016", "Description": "Air Hose Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAV01", "Code": "PNEU009", "Description": "Air Valve Replacement", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAV02", "Code": "PNEU010", "Description": "Air Valve Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAV03", "Code": "PNEU011", "Description": "Air Valve Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEAV04", "Code": "PNEU012", "Description": "Air Valve Overhauling", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEBV01", "Code": "PNEU005", "Description": "Brake Vacuum Removal", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEBV02", "Code": "PNEU006", "Description": "Brake Vacuum Installation", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEBV03", "Code": "PNEU007", "Description": "Brake Vacuum Repairs", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEDV01", "Code": "PNEU001", "Description": "Distribution Valve Removal", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEDV02", "Code": "PNEU002", "Description": "Distribution Valve Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEDV03", "Code": "PNEU003", "Description": "Distribution Valve Replacement", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEDV04", "Code": "PNEU004", "Description": "Distribution Valve Overhauling", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "PNEU", "Symptom_Code": "PNEDV04", "Code": "PNEU018", "Description": "Air coupler Replacement", "Expected_Duration_Hrs": 2.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "DIATF01", "Code": "HIGH01", "Description": "Gear part replacement", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TARPTR300", "Code": "TARP001", "Description": "Tarpaulin Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRAGE01", "Code": "TRAN001", "Description": "Gearbox Removal", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRAGE02", "Code": "TRAN002", "Description": "Gearbox Installation", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRAGE03", "Code": "TRAN003", "Description": "Gearbox Replacement", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRANGK300", "Code": "TRAN005", "Description": "Gear Knob Repair", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRANGK300", "Code": "TRAN006", "Description": "Gear Knob Replacement", "Expected_Duration_Hrs": 0.3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TRAN", "Symptom_Code": "TRANGO000", "Code": "TRAN004", "Description": "Gear Overhaul", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TYRE", "Symptom_Code": "TYRE01", "Code": "TYRE001", "Description": "Tyre Patching", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TYRE", "Symptom_Code": "TYRE02", "Code": "TYRE002", "Description": "Tyre Inflation", "Expected_Duration_Hrs": 0.25, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TYRE", "Symptom_Code": "TYRE03", "Code": "TYRE003", "Description": "Tyre Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TYRE", "Symptom_Code": "TYRER01", "Code": "TYRE004", "Description": "Rim Replacement", "Expected_Duration_Hrs": 0.5, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "TYRE", "Symptom_Code": "TYRER02", "Code": "TYRE005", "Description": "Rim Repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELBB01", "Code": "WELD004", "Description": "Box Body Door", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELCA01", "Code": "WELD006", "Description": "Cabin replacement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELCH01", "Code": "WELD001", "Description": "Chassis Reinforcement", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELCH02", "Code": "WELD003", "Description": "Chassis Fracture Repair", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELCR03", "Code": "WELD015", "Description": "Container Roof Repair", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELDBB000", "Code": "WELD017", "Description": "Back Bumper repair", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELDS01", "Code": "WELD005", "Description": "Drop Side Door", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELDT001", "Code": "WELD019", "Description": "Turner Work", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELFB02", "Code": "WELD010", "Description": "Flooring of Box Body/Container", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELFT01", "Code": "WELD008", "Description": "Fuel Tank (Steel) repair", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELFT02", "Code": "WELD009", "Description": "Fuel Tank (Aluminium)", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELKP01", "Code": "WELD002", "Description": "King Pin Reinforcement", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELRB03", "Code": "WELD011", "Description": "Roofing of Box Body/Container", "Expected_Duration_Hrs": 7, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELRP01", "Code": "WELD016", "Description": "Radiator Protector Installation", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELSI02", "Code": "WELD007", "Description": "Side Impact Bar", "Expected_Duration_Hrs": 4, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELTB03", "Code": "WELD013", "Description": "Trailer Board/Door Hingers", "Expected_Duration_Hrs": 3, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELTD03", "Code": "WELD014", "Description": "Tractor Door Hinges", "Expected_Duration_Hrs": 1, "Spare_Parts_Needed": false},
{"Fault_Area_Code": "WELD", "Symptom_Code": "WELTH03", "Code": "WELD012", "Description": "Trailer Hooks", "Expected_Duration_Hrs": 2, "Spare_Parts_Needed": false},

])

const fault_categories = ref(
  [
    {
      "Code": "DIAG",
      "Description": "Diagnosis"
    },
    {
      "Code": "ELEC",
      "Description": "Electrical"
    },
    {
      "Code": "FABR",
      "Description": "Body and Fabrication"
    },
    {
      "Code": "LUB",
      "Description": "Lubrication"
    },
    {
      "Code": "MECH",
      "Description": "Mechanical"
    },
    {
      "Code": "PAIN",
      "Description": "Painting"
    },
    {
      "Code": "PNEU",
      "Description": "Pneumatic"
    },
    {
      "Code": "TRAN",
      "Description": "Transmission"
    },
    {
      "Code": "TYRE",
      "Description": "Tyre"
    },
    {
      "Code": "WELD",
      "Description": "Welding"
    }
  ]
)



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

async function createJob(){

    const data = {
      truck_number:selectedJobTruckNumber.value,
      fault_area_code: selectedFault.value.Fault_Area_Code,
      symptom_code: selectedFault.value.Symptom_Code,
      fault_code: selectedFault.value.Code,
      expected_job_duration_in_hours: selectedFault.value.Expected_Duration_Hrs,
      spare_parts_needed: selectedFault.value.Spare_Parts_Needed,
      description:selectedFault.value.Description,
      job_technician: selectedTechnician.value.id
    }
    
    console.log(data);
    try{
        
        const response = await $http.post('api/v1/jobs', data)
        
        toast.info(response.data.message, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
    
                showCreateJobModal.value=false;
                selectedFault.value=null
                selectedTechnician.value=null;
                getJobs();
    } catch (error){
        recentJobsLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(createJob);
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

async function cancelJob(){

    const data = {
      job_uuid:selectedJob.value.uuid,
      action: 'cancel',
    }
    
    console.log(data);
    try{
        
        const response = await $http.put('api/v1/jobs', data)
        confirmCancelJobModal.value=false;
        selectedJob.value=null;
        getJobs(null, {'status':status, 'recent':order == 'recent'? true:false})
        toast.info(response.data.message, {
                    autoClose: 3000,
                    position: toast.POSITION.TOP_RIGHT,
                });
                
                
    } catch (error){
        recentJobsLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(cancelJob);
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

async function getJobs(page=null, extraparams=null){
    let params = {}
    recentJobsLoader.value=true;
    try{
        if (page){
        params.page=page;
        }
        if(extraparams){
        params = {...params,...extraparams}
        }

        const response = await $http.get('api/v1/jobs', {params})
        jobs.value = response.data
        if(!Object.keys(params).includes('search_text')){
          searchText.value = '';
        }
        recentJobsLoader.value=false;
    } catch (error){
        recentJobsLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getJobs);
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

async function getTechnicians(page=null, key=null){
    let params={
      role:'job_technician',
    }
    
    try {
      if (page){
        params.page=page;
        }
   
    if(key){
        params['searchText'] = searchTechnicianText.value;
        if(!searchTechnicianText.value){
        return ;
        }
    }
    //isLoading.value=true;
    recentTechniciansLoader.value=true;
    const response = await $http.get('/accounts/staff', {params});
    technicians.value = response.data;
    searchTechnicianText.value=''
   //isLoading.value=false;
   recentTechniciansLoader.value=false;
    } catch (error) {
    
    //isLoading.value=false;
    recentTechniciansLoader.value=false;
            if (error.response) {
                const status = error.response.status;
                if (status === 401) {
                    // Unauthorized access, attempt to refresh token
                    await refreshToken(getTechnicians);
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

async function fetchTrucks(page=null, key=null){
    let params={}
    
    try {
    
    if(page){
        params.page = page;
    }
    if(key){
        params[key] = searchText.value;
        if(!searchText){
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



const filterDescription = (item) => {
  
  if(fault_description.value.trim().length > 0) {
    const searchtext = fault_description.value.trim().toLowerCase();
    
    return item.toLowerCase().includes(searchtext);
  }
}




onMounted(() => {
    store.commit('setCurrentPage', 'job-management')
    getUserData();
    getJobs(null, {'status':'pending', 'recent':false});
    getTechnicians();
    
})

</script>


<template>
    <div class="container-fluid py-4" >

        <div class="row">
          <div class="col-12">
            <div class="card my-4">
              <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                <div class="bg-gradient-secondary  border-radius-lg pt-4 pb-3 d-flex align-items-center" style="justify-content: space-between;padding:0 1rem;">
                  <h6 class="text-white text-capitalize">
                    <span>{{status}}</span>
                    JobsgetJobs(null, {'status':status, 'recent':order == 'recent'? true:false})
                  </h6>
                  <button style="background:var(--bs-primary);color:#fff;border:1px solid var(--bs-primary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="showCreateJobModal=true">Create Job</button>
                </div>
                <div class="searchbar my-3">
                    <input type="text" class="" @keyup.enter="getJobs(null, {'status':status, 'recent':order == 'recent'? true:false, 'search_text':searchText}, )" v-model="searchText" placeholder="Search Table" >
                    <button style="background:var(--bs-success);color:#fff;border:1px solid var(--bs-success);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" @click="getJobs(null, {'status':status, 'recent':order == 'recent'? true:false, 'search_text':searchText},)">Search</button>
                    <button style="background:var(--bs-secondary);color:#fff;border:1px solid var(--bs-secondary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;" class="reset-table" @click="status='pending';order='';">Reset Table</button>
                    
                    
                </div>
                <div class="searchbar my-3">
                    <select name="" id="" v-model="status" @change="getJobs(null, {'status':status, 'recent':order == 'recent'? true:false})">
                        <option value="pending">Pending Jobs</option>
                        <option value="in_progress">Work In-Progress</option>
                        <option value="completed">Completed Jobs</option>
                        <option value="cancelled">Cancelled Jobs</option>
                      </select>
                      <select class="mx-2" id="" v-model="order" @change="getJobs(null, {'status':status, 'recent':order == 'recent'? true:false})">
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
                      <tr v-for="job in jobs.data" :key="item" @click="selectedJob=job" style="cursor:pointer;">
                        <td>
                          <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-primary);">
                              {{job.fault_code}} 
                          </div>
                        </td>
                        <td>
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
                        
                          <span class="text-xs font-weight-bold" style="text-transform: capitalize;">{{job.job_technician.last_name}} {{job.job_technician.first_name}}</span>
                        </td>
                        <td class="align-middle text-center text-sm">
                        
                          <span class="text-xs font-weight-bold" >{{job.expected_job_duration_in_hours > 1 ? job.expected_job_duration_in_hours+" Hrs" : job.expected_job_duration_in_hours+" Hr"  }}</span>
                        </td>
                        <td class="align-middle text-center text-sm">
                          <div class="d-flex px-4 py-1 " >
                              <span class="text-xs font-weight-bold " >{{moment(job.job_added).format("DD MMM, YYYY. hh:mm A")}}</span>
                          </div>
                          
                        </td>
                      </tr>
                     
                    </tbody>
                  </table>
                  <div class="pagination"  v-if="jobs">

                    <div class="controls" v-if="jobs.pagination">
                     <span @click="getJobs(jobs.pagination.current_page - 1)"  v-if="jobs.pagination.current_page > 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span  v-else-if="jobs.pagination.total_pages !== 1">
                       <i class="material-icons">chevron_left</i>
                     </span>
                     <span v-for="i in jobs.pagination.total_pages" :key="i" @click="getJobs(i)" :class="{'active':jobs.pagination.current_page === i}">
                       {{ i }}
                     </span>
                     <span @click="getJobs(jobs.pagination.current_page + 1)" v-if="jobs.pagination.current_page < jobs.pagination.total_pages">
                       <i class="material-icons">chevron_right</i>
                     </span>
                    </div>
                 
                     <div class="pagination-info">
                       <span>Page {{ jobs.pagination.current_page }} of {{ jobs.pagination.total_pages }}</span>
                     </div>
                   </div>
                  <div class="table-loader" v-if="recentJobsLoader">
                    <div class="loader"></div>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        




        <div class="content-modal" v-if="showCreateJobModal">
          <div class="modal-content">
            <div class="close-button">
              <span class="svg-icon"
                ><svg
                  @click="showCreateJobModal = false"
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

            <div class="reg">
              <div class="page-marker">
                <div class="field2">
                  <div class="checklist">
                    <span class="font-weight-bold">
                      <span>Truck Number: </span>
                      <span style="text-decoration: underline; color:var(--bs-blue);cursor:pointer;"><input type="text" placeholder="Truck Number" v-model="selectedJobTruckNumber" @input="selectedJobTruckNumber=selectedJobTruckNumber.toUpperCase()"></span>
                    </span>
                  </div>
                  <div class="checklist">
                    <span class="font-weight-bold " :class="{'d-flex flex-column':!selectedFault}">
                      <span>Fault Description: </span>
                      <input type="text" v-model="fault_description"   placeholder="Type a Fault Description" v-if="!selectedFault">
                      <span class="d-flex" style="color:var(--bs-primary);flex-direction: row;" v-else>
                         <span>{{selectedFault.Description}} </span>
                         <span style="text-decoration: underline; color:var(--bs-blue); margin-left:1rem;cursor:pointer;" @click="fault_description='';selectedFault=null">Clear Description</span>
                      </span>
                    </span>
                  </div>
                  <div class="checklist" v-if="!selectedFault">
                    <ul>
                      <template v-for="item in fault_list" :key="item">
                        <li v-if="filterDescription(item.Description)" @click="selectedFault=item">{{item.Description}}</li>
                      </template>
                    </ul>
                  </div>
                  <div class="checklist d-flex" style="justify-content: space-between;" v-if="selectedFault">
                    <span class="font-weight-bold">
                      <span>Fault Area Code: </span>
                      <span class="text-primary " v-if="selectedFault">{{selectedFault.Fault_Area_Code}} ({{fault_categories[fault_categories.findIndex(item => item.Code === selectedFault.Fault_Area_Code.toUpperCase())].Description}})</span>
                      <span class="text-secondary " v-else>Description not selected</span>
                    </span>
                    <span class="font-weight-bold">
                      <span>Expected Job Duration: </span>
                      <span class="text-primary " v-if="selectedFault">{{selectedFault.Expected_Duration_Hrs > 1 ? selectedFault.Expected_Duration_Hrs+" Hrs" : selectedFault.Expected_Duration_Hrs+" Hr"  }} </span>
                      <span class="text-secondary " v-else>Description not selected</span>
                    </span>
                  </div>
                  
                  <div class="checklist d-flex" style="justify-content: space-between;" v-if="selectedFault">
                    <div  class="d-flex" style="flex-direction: row;justify-content: space-between;">
                      <span class="font-weight-bold">
                        <span>Symptom Code: </span>
                        <span class="text-primary " v-if="selectedFault">{{selectedFault.Symptom_Code}}</span>
                        <span class="text-secondary " v-else>Description not selected</span>
                      </span>
                      <span class="font-weight-bold mx-4">
                        <span>Fault Code: </span>
                        <span class="text-primary " v-if="selectedFault">{{selectedFault.Code}}</span>
                        <span class="text-secondary " v-else>Description not selected</span>
                      </span>
                    </div>
                    <span class="font-weight-bold" >
                      <span>Spare parts needed ?: </span>
                      <span class="text-primary " v-if="selectedFault">{{selectedFault.Spare_Parts_Needed ? "Yes": "No"}}</span>
                      <span class="text-secondary " v-else>Description not selected</span>
                    </span>
                   
                  </div>
                 
                  <div class="checklist">
                    <span class="font-weight-bold">
                      <span>Assigned Technician: </span>
                      <span style="text-decoration: underline; color:var(--bs-blue);cursor:pointer;" @click="getTechnicians();selectTechnicianModal=true;" v-if="!selectedTechnician">Select Technician</span>
                      <span v-else style="text-transform: capitalize;color:var(--bs-dark);">{{selectedTechnician.last_name}} {{selectedTechnician.first_name}}</span> <span v-if="selectedTechnician" style="text-decoration: underline; color:var(--bs-blue);cursor:pointer;margin-left:10px;" @click="getTechnicians();selectTechnicianModal=true;">change Technician</span>
                    </span>
                  </div>
                  <button @click="createJob()" style="background:var(--bs-primary);color:#fff;border:1px solid var(--bs-primary);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;"  class="align-middle text=center" :disabled="!selectedTechnician || !selectedFault || !selectedJobTruckNumber">Submit Job</button>
              

                </div>
              </div>
            </div>

          </div>
        </div>


        <div class="content-modal" v-if="selectedJob">
          <div class="modal-content">
            <div class="close-button">
              <span class="svg-icon"
                ><svg
                  @click="selectedJob = null"
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

            <div class="reg">
              <div class="page-marker">
                <div class="field2">
                  <div class="checklist">
                    <span class="font-weight-bold">
                      <span>Truck Number: </span>
                      <span style=" color:var(--bs-primary);">{{selectedJob.truck_number}}</span>
                    </span>
                  </div>
                  <div class="checklist">
                    <span class="font-weight-bold">
                      <span>Status: </span>
                      <span style=" color:var(--bs-orange);" v-if="selectedJob.status=='pending'">{{selectedJob.status}}</span>
                      <span style=" color:var(--bs-green);" v-else-if="selectedJob.status=='completed'">{{selectedJob.status}}</span>
                      <span style=" color:var(--bs-danger);" v-else-if="selectedJob.status=='cancelled'">{{selectedJob.status}}</span>
                    </span>
                  </div>
                  <div class="checklist">
                    <span class="font-weight-bold ">
                      <span>Fault Description: </span>
                     
                      <span class="" style="color:var(--bs-primary)"> {{selectedJob.description}}</span>
                    </span>
                  </div>
                  
                  <div class="checklist d-flex" style="justify-content: space-between;">
                    <span class="font-weight-bold">
                      <span>Fault Area Code: </span>
                      <span class="text-primary " >{{selectedJob.fault_area_code}} ({{fault_categories[fault_categories.findIndex(item => item.Code === selectedJob.fault_area_code.toUpperCase())].Description}})</span>
                     
                    </span>
                    <span class="font-weight-bold">
                      <span>Expected Job Duration: </span>
                      <span class="text-primary " >{{selectedJob.expected_job_duration_in_hours > 1 ? selectedJob.expected_job_duration_in_hours+" Hrs" : selectedJob.expected_job_duration_in_hours+" Hr"  }} </span>
                     
                    </span>
                  </div>
                  
                  <div class="checklist d-flex" style="justify-content: space-between;" >
                    <div  class="d-flex" style="flex-direction: row;justify-content: space-between;">
                      <span class="font-weight-bold">
                        <span>Symptom Code: </span>
                        <span class="text-primary " >{{selectedJob.symptom_code}}</span>
                       
                      </span>
                      <span class="font-weight-bold">
                        <span>Fault Code: </span>
                        <span class="text-primary " >{{selectedJob.fault_code}}</span>
                       
                      </span>
                    </div>
                    
                    <span class="font-weight-bold" >
                      <span>Spare parts needed ?: </span>
                      <span class="text-primary " >{{selectedJob.spare_parts_needed ? "Yes": "No"}}</span>
                     
                    </span>
                   
                  </div>
                  
                  <div class="checklist">
                    <span class="font-weight-bold">
                      <span>Assigned Technician: </span>
                     
                      <span style="text-transform: capitalize;color:var(--bs-dark);">{{selectedJob.job_technician.last_name}} {{selectedJob.job_technician.first_name}}</span>
                    </span>
                  </div>
                 
                </div>
              </div>
              
            </div>
            <button v-if="selectedJob.status == 'pending'" @click="confirmCancelJobModal=true" style="background:var(--bs-danger);color:#fff;border:1px solid var(--bs-danger);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;"  class="align-middle text=center">Cancel Job</button>
             
          </div>
        </div>


        <div class="content-modal" v-if="selectTechnicianModal">
          <div class="modal-content" style="max-width:50rem;">
            <div class="close-button">
              <span class="svg-icon"
                ><svg
                  @click="selectTechnicianModal = false"
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
            <div class="bg-gradient-secondary  border-radius-lg pt-3 pb-3 d-flex align-items-center header-technicians" style="justify-content: space-between;padding:0 1rem;margin-top:1rem;">
              <h6 class="text-white text-capitalize">
              
                Job Technicians
              </h6>
            <div class="searchbox">
              <input type="text" v-model="searchTechnicianText" placeholder="Search Technicians">
              <button @click="getTechnicians(null, true)" style="background:var(--bs-info);color:#fff;border:1px solid var(--bs-info);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;"><i class="material-icons align-middle text-center">search</i></button>
              <button @click="searchTechnicianText='';getTechnicians()" style="background:var(--bs-danger);color:#fff;border:1px solid var(--bs-danger);margin-left:10px;border-radius: .5rem;padding:.2rem 1rem;"><i class="material-icons align-middle text-center">cancel</i></button>
               
            </div>
            </div>
            <div class="card-body px-0 pb-2 pt-2">
              <div class="table-responsive p-0">
                <table class="table align-items-center mb-0">
                  <thead>
                    <tr >
                      <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Job Technician Name</th>
                      <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Employee_number</th>

                      <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2 align-middle text-center" >Assigned Job</th>

                      <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"></th>
                     
                    </tr>
                  </thead>
                  <tbody v-if="technicians && technicians.data.length > 0">
                    <tr v-for="item in technicians.data" :key="item" @click="selectedTechnician=item;selectTechnicianModal=false">
                      <td>
                        <div class="d-flex px-4 py-1 font-weight-bold" style="color:var(--bs-dark);text-transform:capitalize;">
                          {{item.last_name}} {{item.first_name}}
                        </div>
                      </td>
                   
                      <td class="align-middle text-center font-weight-bold">
                        {{ item.Employee_number || '-' }}
                      </td>
                     
                      
                      <td class="align-middle text-center text-sm">
                      
                        <span class="text-xs font-weight-bold " >{{item.assigned_tasks}}</span>
                      </td>
                      
                    <td class="align-middle text-center text-sm">
                      <span class="custombutton align-middle text-center text-sm bg-gradient-info text-white p-2" style="cursor: pointer;border-radius:.5rem;" @click="selectedTechnician=item;selectTechnicianModal=false">Assign Technician</span>
                    </td>
                    </tr>
                   
                  </tbody>
                </table>
                <div class="pagination"  v-if="technicians">

                  <div class="controls" v-if="technicians.pagination">
                   <span @click="getTechnicians(technicians.pagination.current_page - 1)"  v-if="technicians.pagination.current_page > 1">
                     <i class="material-icons">chevron_left</i>
                   </span>
                   <span  v-else-if="technicians.pagination.total_pages !== 1">
                     <i class="material-icons">chevron_left</i>
                   </span>
                   <span v-for="i in technicians.pagination.total_pages" :key="i" @click="getTechnicians(i)" :class="{'active':technicians.pagination.current_page === i}">
                     {{ i }}
                   </span>
                   <span @click="getTechnicians(technicians.pagination.current_page + 1)" v-if="technicians.pagination.current_page < technicians.pagination.total_pages">
                     <i class="material-icons">chevron_right</i>
                   </span>
                  </div>
               
                   <div class="pagination-info">
                     <span>Page {{ technicians.pagination.current_page }} of {{ technicians.pagination.total_pages }}</span>
                   </div>
                 </div>
                <div class="table-loader" v-if="recentTechniciansLoader">
                  <div class="loader"></div>
              </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="content-modal" v-if="confirmCancelJobModal">
          <div class="modal-content">
            <h2>Confirm Job Cancellation?</h2>
            <p>Are you sure you want to cancel this Job?</p>
            <div class="buttonbox" style="display: flex;justify-content: space-between;">
              <button @click="confirmCancelJobModal=false;" style="background-color: var(--bs-danger);margin:0 1rem;">Go Back</button>
              <button @click="cancelJob(selectedJob)" class="bg-success" style="margin:0 1rem;">Cancel Job</button>
            </div>
            {{ selectedTruckData }}
          </div>
  
        </div>
    

        <div class="loading" v-if="isLoading">
          <div class="loader"></div>
      </div>
      </div>
</template>


<style scoped lang="scss">

table tr{
  
  &:hover{
    background:var(--bs-light);
  }
}


select, input, textarea{
    color:var(--bs-dark);
    border:1px solid var(--bs-gray) !important;
    border-radius: .5rem;
    padding:.2rem .5rem !important;
  }


  .checklist{
    ul{
      padding:0;
      max-height:15rem;
      overflow: auto;
      margin-top: -1rem;
      
       li{
        list-style:none;
        padding:.5rem;
        cursor:pointer;
        background:var(--bs-light);
        margin:.5rem 0;
        border-radius:.5rem;

        &:hover{
          background: var(--bs-primary);
          color: var(--bs-white);
        }
       }
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
      max-width: 45rem;
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
      
      width:1.5rem;
      height:1.5rem;
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
      background: var(--background);
    }
  }
  

  
@media screen and (max-width: 600px) {
  
  .checklist, .checklist span:first{
    display:flex;
    flex-direction: column;
    
  }
  .header-technicians{
    flex-direction: column;

    .searchbox{
      display:flex;
      align-items:flex-end;

      input{
        max-height:35px;
      }
    }
  }
  .reset-table{
    margin:1rem 0 !important;
  }

    .searchbar:nth-child(3){
        display:flex;
        flex-direction: row;
        justify-content: space-between;

        select{
            width:100%;
            margin:.5rem .2rem !important;
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
      margin-top:-4rem;
      #reg,.reg {
        overflow-y: auto;
        max-height: 35rem;
        
       
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
// import axios from 'axios';

// const apiClient = axios.create({
//   baseURL: 'http://localhost:8000', 
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// export const createJob = (ticker) => {
//   return apiClient.post('/jobs', { ticker });
// };

// export const getJob = (jobId) => {
//   return apiClient.get(`/jobs/${jobId}`);
// };


// export const getJobsHistory = () => {
//   return apiClient.get('/jobs');
// };




import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

export const createJob = (ticker) => apiClient.post('/jobs', { ticker });
export const getJob = (jobId) => apiClient.get(`/jobs/${jobId}`);
export const getJobsHistory = () => apiClient.get('/jobs');
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createJob = (ticker) => {
  return apiClient.post('/jobs', { ticker });
};

export const getJob = (jobId) => {
  return apiClient.get(`/jobs/${jobId}`);
};


export const getJobsHistory = () => {
  return apiClient.get('/jobs');
};
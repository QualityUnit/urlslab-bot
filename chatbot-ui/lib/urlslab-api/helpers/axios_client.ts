import axios, {AxiosInstance} from 'axios';
import {HTTPValidationError} from "@/lib/urlslab-api/models/HttpError";

if (!process.env.URLSLAB_BOT_API_KEY) {
  throw new Error("Please provide process.env.URLSLAB_BOT_API_KEY");
}

const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_URLSLAB_BOT_BASE_URL,
  timeout: 1000,
});

// Add Authorization header
axiosInstance.defaults.headers.common['X-API-Key'] = process.env.URLSLAB_BOT_API_KEY;

// Add a response interceptor
axiosInstance.interceptors.response.use(
  response => {
    // Any status code that lies within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  },
  error => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Convert the error response into a structured error
    if (error.response) {
      // The server responded with a status code and data
      // that falls out of the range of 2xx
      const httpError: HTTPValidationError = {
        detail: error.response.data.detail || [],
      };
      return Promise.reject(httpError);
    } else if (error.request) {
      // The request was made but no response was received
      return Promise.reject(new Error('The request was made but no response was received'));
    } else {
      // Something happened in setting up the request that triggered an Error
      return Promise.reject(new Error('Error: ' + error.message));
    }
  },
);

export default axiosInstance;
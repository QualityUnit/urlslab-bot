import axios, {AxiosInstance} from 'axios';

const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_URLSLAB_BOT_BASE_URL,
  timeout: 1000,
});

export default axiosInstance;
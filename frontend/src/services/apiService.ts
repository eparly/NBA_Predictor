import axios from 'axios'

const api = axios.create({
    baseURL: 'https://v5soamuhm6.execute-api.ca-central-1.amazonaws.com/prod',
    headers: {
        'Content-Type': 'application/json'
    }
})

export const getData = async (endpoint: string, params?: Record<string, string>) => {
    try {
        const response = await api.get(endpoint, { params })
        return response.data
    } catch (error) {
        // console.error('Error fetching data: ', error)
        throw error
    }
}
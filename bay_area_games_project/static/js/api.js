/**
 * API调用工具类
 */
const api = {
    baseURL: '',

    /**
     * 获取CSRF Token
     */
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    },

    /**
     * 发送请求
     */
    async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
            },
            credentials: 'include',
        };

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {}),
            },
        };

        try {
            const response = await fetch(this.baseURL + url, finalOptions);
            
            // 处理空响应（如DELETE请求）
            const contentType = response.headers.get('content-type');
            let data = null;
            
            if (contentType && contentType.includes('application/json')) {
                const text = await response.text();
                if (text) {
                    try {
                        data = JSON.parse(text);
                    } catch (e) {
                        console.warn('JSON解析失败:', text);
                    }
                }
            }

            if (!response.ok) {
                // 创建错误对象，包含response信息
                const error = new Error(data?.detail || data?.error || `HTTP ${response.status}`);
                error.response = {
                    status: response.status,
                    statusText: response.statusText,
                    data: data
                };
                throw error;
            }

            return data || {};
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    },

    /**
     * GET请求
     */
    async get(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        return this.request(fullUrl, { method: 'GET' });
    },

    /**
     * POST请求
     */
    async post(url, data = {}) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    /**
     * PUT请求
     */
    async put(url, data = {}) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    /**
     * PATCH请求
     */
    async patch(url, data = {}) {
        return this.request(url, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },

    /**
     * DELETE请求
     */
    async delete(url) {
        return this.request(url, { method: 'DELETE' });
    },
};


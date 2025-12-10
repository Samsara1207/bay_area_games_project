/**
 * 主JavaScript文件
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initTooltips();
    
    // 初始化模态框关闭事件
    initModalClose();
});

/**
 * 初始化工具提示
 */
function initTooltips() {
    // 可以在这里添加工具提示功能
}

/**
 * 初始化模态框关闭事件（点击外部关闭）
 */
function initModalClose() {
    window.onclick = function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    };
}

/**
 * 格式化日期
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
    });
}

/**
 * 格式化日期时间
 */
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * 显示成功消息
 */
function showSuccess(message) {
    showMessage(message, 'success');
}

/**
 * 显示错误消息
 */
function showError(message) {
    showMessage(message, 'error');
}

/**
 * 显示消息
 */
function showMessage(message, type = 'info') {
    // 创建消息元素
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // 插入到页面顶部
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        // 3秒后自动移除
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}

/**
 * 确认对话框
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}


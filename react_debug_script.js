// React应用调试脚本
// 在浏览器控制台中运行此脚本来调试前端问题

console.log("🧪 开始React应用调试...");

// 调试配置
const DEBUG_CONFIG = {
    backendUrl: 'http://127.0.0.1:8000',
    testMessage: '这是一个调试测试消息',
    enableDetailedLogging: true
};

// 工具函数
const debugUtils = {
    log: (message, data = null) => {
        if (DEBUG_CONFIG.enableDetailedLogging) {
            console.log(`🔍 [DEBUG] ${message}`, data || '');
        }
    },
    
    error: (message, error = null) => {
        console.error(`❌ [ERROR] ${message}`, error || '');
    },
    
    success: (message, data = null) => {
        console.log(`✅ [SUCCESS] ${message}`, data || '');
    },
    
    warn: (message, data = null) => {
        console.warn(`⚠️ [WARNING] ${message}`, data || '');
    }
};

// 1. 检查React应用状态
function checkReactApp() {
    debugUtils.log("检查React应用状态...");
    
    // 检查React是否加载
    if (typeof React !== 'undefined') {
        debugUtils.success("React已加载", React.version);
    } else {
        debugUtils.warn("React未在全局作用域中找到");
    }
    
    // 检查React DOM
    if (typeof ReactDOM !== 'undefined') {
        debugUtils.success("ReactDOM已加载");
    } else {
        debugUtils.warn("ReactDOM未在全局作用域中找到");
    }
    
    // 检查应用根元素
    const rootElement = document.getElementById('root');
    if (rootElement) {
        debugUtils.success("找到React根元素", rootElement);
        debugUtils.log("根元素内容长度", rootElement.innerHTML.length);
    } else {
        debugUtils.error("未找到React根元素");
    }
}

// 2. 检查网络连接
async function checkNetworkConnection() {
    debugUtils.log("检查网络连接...");
    
    try {
        // 检查后端连接
        const response = await fetch(`${DEBUG_CONFIG.backendUrl}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            debugUtils.success("后端连接正常", data);
            return true;
        } else {
            debugUtils.error(`后端连接失败: ${response.status}`);
            return false;
        }
    } catch (error) {
        debugUtils.error("网络连接错误", error);
        return false;
    }
}

// 3. 测试API调用
async function testApiCall() {
    debugUtils.log("测试API调用...");
    
    const testData = {
        prompt: DEBUG_CONFIG.testMessage
    };
    
    try {
        debugUtils.log("发送请求", testData);
        
        const startTime = Date.now();
        const response = await fetch(`${DEBUG_CONFIG.backendUrl}/ask_professor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        debugUtils.log(`请求耗时: ${duration}ms`);
        debugUtils.log("响应状态", response.status);
        debugUtils.log("响应头", Object.fromEntries(response.headers.entries()));
        
        if (response.ok) {
            const result = await response.json();
            debugUtils.success("API调用成功", result);
            
            // 验证响应格式
            const requiredFields = ['answer', 'source'];
            const missingFields = requiredFields.filter(field => !(field in result));
            
            if (missingFields.length === 0) {
                debugUtils.success("响应格式正确");
                return result;
            } else {
                debugUtils.error("响应格式错误，缺少字段", missingFields);
                return null;
            }
        } else {
            const errorText = await response.text();
            debugUtils.error(`API调用失败: ${response.status}`, errorText);
            return null;
        }
    } catch (error) {
        debugUtils.error("API调用异常", error);
        return null;
    }
}

// 4. 检查React组件状态
function checkReactComponents() {
    debugUtils.log("检查React组件状态...");
    
    // 尝试找到React Fiber节点
    const rootElement = document.getElementById('root');
    if (rootElement && rootElement._reactInternalFiber) {
        debugUtils.success("找到React Fiber节点");
    } else if (rootElement && rootElement._reactInternalInstance) {
        debugUtils.success("找到React实例");
    } else {
        debugUtils.warn("未找到React内部节点");
    }
    
    // 检查是否有错误边界
    const errorElements = document.querySelectorAll('[data-reactroot] *');
    debugUtils.log(`找到 ${errorElements.length} 个React元素`);
    
    // 检查控制台错误
    const originalError = console.error;
    let errorCount = 0;
    console.error = function(...args) {
        errorCount++;
        originalError.apply(console, args);
    };
    
    setTimeout(() => {
        console.error = originalError;
        if (errorCount > 0) {
            debugUtils.warn(`检测到 ${errorCount} 个控制台错误`);
        } else {
            debugUtils.success("没有检测到控制台错误");
        }
    }, 1000);
}

// 5. 模拟用户交互
function simulateUserInteraction() {
    debugUtils.log("模拟用户交互...");
    
    // 查找输入框
    const inputElements = document.querySelectorAll('input[type="text"], textarea');
    debugUtils.log(`找到 ${inputElements.length} 个输入元素`);
    
    // 查找按钮
    const buttonElements = document.querySelectorAll('button');
    debugUtils.log(`找到 ${buttonElements.length} 个按钮元素`);
    
    // 查找发送按钮
    const sendButtons = Array.from(buttonElements).filter(btn => 
        btn.textContent.includes('发送') || 
        btn.textContent.includes('Send') ||
        btn.className.includes('send')
    );
    
    if (sendButtons.length > 0) {
        debugUtils.success(`找到 ${sendButtons.length} 个发送按钮`, sendButtons);
    } else {
        debugUtils.warn("未找到发送按钮");
    }
    
    return {
        inputs: inputElements,
        buttons: buttonElements,
        sendButtons: sendButtons
    };
}

// 6. 检查消息列表
function checkMessageList() {
    debugUtils.log("检查消息列表...");
    
    // 查找消息容器
    const messageContainers = document.querySelectorAll('[class*="message"], [class*="chat"], [id*="message"], [id*="chat"]');
    debugUtils.log(`找到 ${messageContainers.length} 个可能的消息容器`);
    
    // 查找具体的消息元素
    const messageElements = document.querySelectorAll('[class*="user-message"], [class*="ai-message"], [class*="bot-message"]');
    debugUtils.log(`找到 ${messageElements.length} 个消息元素`);
    
    if (messageElements.length > 0) {
        debugUtils.success("找到消息元素", Array.from(messageElements).map(el => el.textContent.substring(0, 50)));
    }
    
    return {
        containers: messageContainers,
        messages: messageElements
    };
}

// 7. 完整的调试流程
async function runFullDebug() {
    console.log("🚀 开始完整的React应用调试流程...");
    console.log("=" * 60);
    
    // 1. 检查React应用
    checkReactApp();
    
    // 2. 检查网络连接
    const networkOk = await checkNetworkConnection();
    
    // 3. 测试API调用
    let apiResult = null;
    if (networkOk) {
        apiResult = await testApiCall();
    }
    
    // 4. 检查React组件
    checkReactComponents();
    
    // 5. 模拟用户交互
    const uiElements = simulateUserInteraction();
    
    // 6. 检查消息列表
    const messageInfo = checkMessageList();
    
    // 生成调试报告
    console.log("\n📊 调试报告:");
    console.log("=" * 40);
    console.log(`网络连接: ${networkOk ? '✅ 正常' : '❌ 异常'}`);
    console.log(`API调用: ${apiResult ? '✅ 成功' : '❌ 失败'}`);
    console.log(`输入元素: ${uiElements.inputs.length} 个`);
    console.log(`按钮元素: ${uiElements.buttons.length} 个`);
    console.log(`发送按钮: ${uiElements.sendButtons.length} 个`);
    console.log(`消息容器: ${messageInfo.containers.length} 个`);
    console.log(`消息元素: ${messageInfo.messages.length} 个`);
    
    // 提供修复建议
    console.log("\n💡 修复建议:");
    if (!networkOk) {
        console.log("- 检查后端服务器是否运行");
        console.log("- 检查CORS配置");
    }
    if (!apiResult) {
        console.log("- 检查API端点配置");
        console.log("- 检查请求格式");
    }
    if (uiElements.sendButtons.length === 0) {
        console.log("- 检查发送按钮的渲染");
        console.log("- 检查按钮的事件绑定");
    }
    if (messageInfo.messages.length === 0) {
        console.log("- 检查消息列表的渲染");
        console.log("- 检查消息状态管理");
    }
    
    return {
        networkOk,
        apiResult,
        uiElements,
        messageInfo
    };
}

// 8. 实时监控函数
function startRealtimeMonitoring() {
    debugUtils.log("启动实时监控...");
    
    // 监控DOM变化
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                const addedElements = Array.from(mutation.addedNodes).filter(node => node.nodeType === 1);
                if (addedElements.length > 0) {
                    debugUtils.log("DOM元素已添加", addedElements.map(el => el.tagName || el.textContent?.substring(0, 30)));
                }
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    debugUtils.success("实时监控已启动");
    
    // 返回停止监控的函数
    return () => {
        observer.disconnect();
        debugUtils.log("实时监控已停止");
    };
}

// 导出调试函数到全局作用域
window.debugReactApp = {
    runFullDebug,
    checkReactApp,
    checkNetworkConnection,
    testApiCall,
    checkReactComponents,
    simulateUserInteraction,
    checkMessageList,
    startRealtimeMonitoring,
    utils: debugUtils
};

// 自动运行基础检查
console.log("🎯 React调试脚本已加载");
console.log("💡 使用方法:");
console.log("   debugReactApp.runFullDebug() - 运行完整调试");
console.log("   debugReactApp.startRealtimeMonitoring() - 启动实时监控");
console.log("   debugReactApp.testApiCall() - 测试API调用");

// 自动运行完整调试
setTimeout(() => {
    runFullDebug();
}, 1000);

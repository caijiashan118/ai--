// 字段选择器调试脚本
console.log('=== 字段选择器调试开始 ===');

// 检查必要的元素
function checkElements() {
    console.log('1. 检查DOM元素...');
    
    const container = document.getElementById('columnSelectorButtons');
    console.log('columnSelectorButtons容器:', container ? '存在' : '不存在');
    
    const collapse = document.getElementById('columnSelector');
    console.log('columnSelector折叠面板:', collapse ? '存在' : '不存在');
    
    const summaryTab = document.getElementById('summary-tab');
    console.log('summary-tab标签:', summaryTab ? '存在' : '不存在');
    
    return container && collapse;
}

// 检查变量定义
function checkVariables() {
    console.log('2. 检查变量定义...');
    
    console.log('COLUMN_DEFINITIONS:', typeof COLUMN_DEFINITIONS !== 'undefined' ? '已定义' : '未定义');
    if (typeof COLUMN_DEFINITIONS !== 'undefined') {
        console.log('COLUMN_DEFINITIONS长度:', COLUMN_DEFINITIONS.length);
    }
    
    console.log('availableColumns:', typeof availableColumns !== 'undefined' ? '已定义' : '未定义');
    if (typeof availableColumns !== 'undefined') {
        console.log('availableColumns长度:', availableColumns.length);
    }
    
    console.log('columnVisibility:', typeof columnVisibility !== 'undefined' ? '已定义' : '未定义');
    if (typeof columnVisibility !== 'undefined') {
        console.log('columnVisibility键数量:', Object.keys(columnVisibility).length);
    }
}

// 检查函数定义
function checkFunctions() {
    console.log('3. 检查函数定义...');
    
    console.log('initializeColumnSelector:', typeof initializeColumnSelector === 'function' ? '已定义' : '未定义');
    console.log('generateColumnSelectorButtons:', typeof generateColumnSelectorButtons === 'function' ? '已定义' : '未定义');
    console.log('toggleColumnVisibility:', typeof toggleColumnVisibility === 'function' ? '已定义' : '未定义');
    console.log('applyColumnSelection:', typeof applyColumnSelection === 'function' ? '已定义' : '未定义');
}

// 测试初始化
function testInitialization() {
    console.log('4. 测试初始化...');
    
    if (typeof initializeColumnSelector === 'function') {
        try {
            const result = initializeColumnSelector();
            console.log('初始化结果:', result);
        } catch (error) {
            console.error('初始化失败:', error);
        }
    } else {
        console.error('initializeColumnSelector函数未定义');
    }
}

// 检查表格状态
function checkTableStatus() {
    console.log('5. 检查表格状态...');
    
    console.log('summaryTable:', typeof summaryTable !== 'undefined' ? '已定义' : '未定义');
    if (typeof summaryTable !== 'undefined') {
        console.log('summaryTable类型:', typeof summaryTable);
    }
    
    console.log('summaryLoaded:', typeof summaryLoaded !== 'undefined' ? summaryLoaded : '未定义');
}

// 检查事件监听器
function checkEventListeners() {
    console.log('6. 检查事件监听器...');
    
    const summaryTab = document.getElementById('summary-tab');
    if (summaryTab) {
        console.log('summary-tab元素存在，检查点击事件...');
        // 这里无法直接检查事件监听器，但可以测试点击
    } else {
        console.log('summary-tab元素不存在');
    }
}

// 手动触发初始化
function manualInit() {
    console.log('7. 手动触发初始化...');
    
    if (typeof initializeColumnSelector === 'function') {
        console.log('尝试手动初始化...');
        const result = initializeColumnSelector();
        console.log('手动初始化结果:', result);
        
        if (result) {
            console.log('手动初始化成功，检查按钮生成...');
            const container = document.getElementById('columnSelectorButtons');
            if (container) {
                console.log('容器子元素数量:', container.children.length);
                console.log('容器HTML:', container.innerHTML.substring(0, 200) + '...');
            }
        }
    } else {
        console.error('initializeColumnSelector函数不可用');
    }
}

// 运行所有检查
function runAllChecks() {
    console.log('开始运行字段选择器调试...');
    
    checkElements();
    checkVariables();
    checkFunctions();
    checkTableStatus();
    checkEventListeners();
    manualInit();
    
    console.log('=== 字段选择器调试结束 ===');
}

// 页面加载完成后运行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAllChecks);
} else {
    runAllChecks();
}

// 导出函数供手动调用
window.debugFieldSelector = runAllChecks;

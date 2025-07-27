
// 音频播放功能测试脚本
// 在浏览器控制台中运行

console.log("🎵 开始音频播放功能测试...");

function testAudioControls() {
    console.log("🔍 检查音频控件...");
    
    // 查找音频播放按钮
    const audioButtons = document.querySelectorAll('button[title*="播放"], button[title*="暂停"], button[title*="继续"]');
    
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频控件`);
        
        audioButtons.forEach((button, index) => {
            const title = button.getAttribute('title');
            const isDisabled = button.disabled;
            const classes = button.className;
            
            console.log(`音频按钮 ${index + 1}:`);
            console.log(`  标题: ${title}`);
            console.log(`  禁用: ${isDisabled ? '是' : '否'}`);
            console.log(`  样式: ${classes.includes('bg-blue') ? '蓝色(活跃)' : '灰色(默认)'}`);
        });
        
        return true;
    } else {
        console.log("❌ 未找到音频控件");
        return false;
    }
}

function testReplayButtons() {
    console.log("🔍 检查重播按钮...");
    
    const replayButtons = document.querySelectorAll('button[title*="重新播放"], button[title*="重播"]');
    
    if (replayButtons.length > 0) {
        console.log(`✅ 找到 ${replayButtons.length} 个重播按钮`);
        
        replayButtons.forEach((button, index) => {
            const isVisible = button.offsetParent !== null;
            const isDisabled = button.disabled;
            
            console.log(`重播按钮 ${index + 1}:`);
            console.log(`  可见: ${isVisible ? '是' : '否'}`);
            console.log(`  禁用: ${isDisabled ? '是' : '否'}`);
        });
        
        return true;
    } else {
        console.log("ℹ️  暂无重播按钮（需要先播放音频）");
        return true; // 这是正常的，因为重播按钮只在有音频时显示
    }
}

function testLoadingStates() {
    console.log("🔍 检查加载状态...");
    
    // 查找加载动画
    const loadingAnimations = document.querySelectorAll('.animate-spin');
    
    if (loadingAnimations.length > 0) {
        console.log(`ℹ️  发现 ${loadingAnimations.length} 个加载动画（可能正在生成音频）`);
    } else {
        console.log("✅ 当前无加载状态");
    }
    
    // 查找状态文字
    const statusTexts = document.querySelectorAll('span:contains("生成中"), span:contains("播放失败")');
    
    if (statusTexts.length > 0) {
        console.log(`⚠️  发现 ${statusTexts.length} 个状态文字（应该已移除）`);
        return false;
    } else {
        console.log("✅ 状态文字已正确移除");
        return true;
    }
}

async function simulateAudioTest() {
    console.log("🎭 模拟音频测试...");
    
    // 查找第一个音频播放按钮
    const audioButton = document.querySelector('button[title*="播放"]');
    
    if (audioButton) {
        console.log("📝 找到音频播放按钮");
        console.log("💡 提示: 可以手动点击测试以下功能:");
        console.log("   1. 点击扬声器图标开始播放");
        console.log("   2. 观察按钮变为加载动画");
        console.log("   3. 音频开始播放后变为暂停按钮");
        console.log("   4. 点击暂停按钮测试暂停功能");
        console.log("   5. 再次点击测试继续播放功能");
        console.log("   6. 查看是否出现重播按钮");
        
        return true;
    } else {
        console.log("❌ 未找到音频播放按钮");
        console.log("💡 请先发送消息获得AI回复");
        return false;
    }
}

function generateTestReport() {
    console.log("📊 生成测试报告...");
    
    const results = {
        audioControls: testAudioControls(),
        replayButtons: testReplayButtons(),
        loadingStates: testLoadingStates()
    };
    
    console.log("\n📋 音频功能测试结果:");
    console.log("   音频控件:", results.audioControls ? '✅ 正常' : '❌ 异常');
    console.log("   重播按钮:", results.replayButtons ? '✅ 正常' : '❌ 异常');
    console.log("   加载状态:", results.loadingStates ? '✅ 正常' : '❌ 异常');
    
    const passedTests = Object.values(results).filter(Boolean).length;
    const totalTests = Object.keys(results).length;
    
    console.log(`\n📈 测试通过率: ${passedTests}/${totalTests} (${Math.round(passedTests/totalTests*100)}%)`);
    
    if (passedTests === totalTests) {
        console.log("🎉 音频播放功能修复验证通过！");
    } else {
        console.log("⚠️  部分功能需要进一步检查");
    }
    
    return results;
}

// 运行测试
setTimeout(() => {
    console.log("🚀 开始运行音频功能测试...");
    
    // 生成测试报告
    setTimeout(() => generateTestReport(), 500);
    
    // 模拟测试指导
    setTimeout(() => simulateAudioTest(), 1000);
}, 500);

console.log("🎯 音频播放功能测试脚本已加载");
console.log("💡 请发送消息获得AI回复，然后测试音频播放功能");

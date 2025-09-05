// static/script.js

// static/script.js

// ページのすべてのコンテンツが読み込まれた後に、この中の処理を実行する
document.addEventListener('DOMContentLoaded', function() {
    
    // --- 日付の自動入力 ---
    // idが 'visitDate' の要素（日付入力欄）を取得
    const visitDateInput = document.getElementById('visitDate');
    
    // もし、その要素が存在するなら（詳細ページを開いているなら）
    if (visitDateInput) {
        // 今日の日付を取得
        const today = new Date();
        
        // YYYY-MM-DD 形式の文字列に変換
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0'); // 月は0から始まるので+1
        const day = String(today.getDate()).padStart(2, '0');
        const todayString = `${year}-${month}-${day}`;
        
        // 日付入力欄の初期値として設定
        visitDateInput.value = todayString;
    }

});
document.addEventListener('DOMContentLoaded', function() {
    const filterCheckboxes = document.querySelectorAll('.pub-filter-checkbox');
    const publicationItems = document.querySelectorAll('.publication-ol li.publication');
    
    // ------------------------------------------------------
    // 1. 核心篩選函式 (修改為 AND/OR 邏輯)
    // ------------------------------------------------------
    function filterPublications() {
        
        // 1. 收集並按組別分組選中的篩選條件
        const activeFiltersByGroup = {};
        filterCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const group = checkbox.getAttribute('data-group'); // 'year' 或 'tag'
                const filter = checkbox.getAttribute('data-filter');
                
                if (!activeFiltersByGroup[group]) {
                    activeFiltersByGroup[group] = [];
                }
                activeFiltersByGroup[group].push(filter);
            }
        });
        
        // 獲取所有篩選組的名稱 (e.g., ['year', 'tag'])
        const filterGroups = Object.keys(activeFiltersByGroup);

        // 如果沒有選中任何篩選條件，則顯示所有項目
        if (filterGroups.length === 0) {
            publicationItems.forEach(item => item.style.display = '');
            return;
        }

        // 2. 遍歷所有出版物項目，進行 AND/OR 檢查
        publicationItems.forEach(item => {
            const itemTags = item.getAttribute('data-tags')
                                 .split(' ')
                                 .filter(tag => tag.length > 0);
            
            // 預設假設該項目通過篩選
            let passesAllGroups = true;
            
            // 遍歷所有選中的篩選組 (例如 Year Group, Tag Group)
            for (const group of filterGroups) {
                const activeFilters = activeFiltersByGroup[group];
                
                // 檢查該組別的條件是否被滿足 (組內使用 OR 邏輯)
                // 只要文章的標籤中包含該組別的任一篩選條件，即通過該組別
                const passesGroup = activeFilters.some(filter => itemTags.includes(filter));
                
                // 如果文章不通過該組別的篩選，則不通過總篩選 (組間使用 AND 邏輯)
                if (!passesGroup) {
                    passesAllGroups = false;
                    break; 
                }
            }

            // 3. 根據最終結果顯示或隱藏項目
            if (passesAllGroups) {
                item.style.display = ''; // 顯示
            } else {
                item.style.display = 'none'; // 隱藏
            }
        });
    }

    // 2. 事件監聽：當任何 checkbox 改變時觸發篩選
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterPublications);
    });
    
    // ... (保留原有的展開/收合邏輯) ...
    const yearCollapseButton = document.getElementById('filter-year');
    const yearList = document.getElementById('filter-year-list');

    if (yearCollapseButton && yearList) {
        yearCollapseButton.addEventListener('click', function() {
            const isCollapsed = yearList.style.display === 'none';
            yearList.style.display = isCollapsed ? 'block' : 'none';
            // 更改箭頭方向
            const icon = yearCollapseButton.querySelector('i');
            icon.classList.toggle('fa-chevron-right', !isCollapsed);
            icon.classList.toggle('fa-chevron-down', isCollapsed);
        });
        
        // 預設收合
        yearList.style.display = 'none';
    }
});
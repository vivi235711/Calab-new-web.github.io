document.addEventListener('DOMContentLoaded', function() {
    const filterCheckboxes = document.querySelectorAll('.pub-filter-checkbox');
    const publicationItems = document.querySelectorAll('.publication-ol li.publication');
    
    /**
     * Core filtering function (Modified for AND/OR logic)
     */
    function filterPublications() {
        
        // 1. Collect and group selected filters by group (e.g., 'year', 'tag')
        const activeFiltersByGroup = {};
        filterCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const group = checkbox.getAttribute('data-group'); // 'year' or 'tag'
                const filter = checkbox.getAttribute('data-filter');
                
                if (!activeFiltersByGroup[group]) {
                    activeFiltersByGroup[group] = [];
                }
                activeFiltersByGroup[group].push(filter);
            }
        });
        
        // Get names of all active filter groups (e.g., ['year', 'tag'])
        const filterGroups = Object.keys(activeFiltersByGroup);

        // If no filters are selected, show all items
        if (filterGroups.length === 0) {
            publicationItems.forEach(item => item.style.display = '');
            return;
        }

        // 2. Iterate through all publication items for AND/OR check
        publicationItems.forEach(item => {
            const itemTags = item.getAttribute('data-tags')
                                 .split(' ')
                                 .filter(tag => tag.length > 0);
            
            // Default assumption is the item passes the filter
            let passesAllGroups = true;
            
            // Iterate through each active filter group (e.g., Year Group, Tag Group)
            for (const group of filterGroups) {
                const activeFilters = activeFiltersByGroup[group];
                
                // Check if the group condition is met (OR logic within the group)
                // Pass if any tag in the article matches any filter in the group
                const passesGroup = activeFilters.some(filter => itemTags.includes(filter));
                
                // Fail general filter if group check fails (AND logic between groups)
                if (!passesGroup) {
                    passesAllGroups = false;
                    break; 
                }
            }

            // 3. Show or hide item based on filtering results
            if (passesAllGroups) {
                item.style.display = ''; // Show
            } else {
                item.style.display = 'none'; // Hide
            }
        });
    }

    // 2. Event Listener: Trigger filtering when any checkbox changes
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterPublications);
    });
    
    // ... (Retain existing expand/collapse logic) ...
    const yearCollapseButton = document.getElementById('filter-year');
    const yearList = document.getElementById('filter-year-list');

    if (yearCollapseButton && yearList) {
        yearCollapseButton.addEventListener('click', function() {
            const isCollapsed = yearList.style.display === 'none';
            yearList.style.display = isCollapsed ? 'block' : 'none';
            // Toggle arrow direction
            const icon = yearCollapseButton.querySelector('i');
            icon.classList.toggle('fa-chevron-right', !isCollapsed);
            icon.classList.toggle('fa-chevron-down', isCollapsed);
        });
        
        // Collapse by default
        yearList.style.display = 'none';
    }
});
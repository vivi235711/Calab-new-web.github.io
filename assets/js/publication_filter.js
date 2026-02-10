document.addEventListener('DOMContentLoaded', function() {
    const filterCheckboxes = document.querySelectorAll('.pub-filter-checkbox');
    const publicationItems = document.querySelectorAll('.publication-ol li.publication');
    const clearAllBtn = document.getElementById('clear-all-filters');

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
            publicationItems.forEach(item => {
                item.style.display = '';
                item.classList.remove('fade-out');
                item.classList.add('fade-in');
            });
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
                let passesGroup;

                if (group === 'tag') {
                    // Tag group uses AND logic (must have ALL selected tags)
                    passesGroup = activeFilters.every(filter => itemTags.includes(filter));
                } else {
                    // Other groups (like Year) use OR logic (must have at least one selected value)
                    passesGroup = activeFilters.some(filter => itemTags.includes(filter));
                }

                // Fail general filter if group check fails (AND logic between groups)
                if (!passesGroup) {
                    passesAllGroups = false;
                    break;
                }
            }

            // 3. Show or hide item based on filtering results
            if (passesAllGroups) {
                item.style.display = '';
                item.classList.remove('fade-out');
                item.classList.add('fade-in');
            } else {
                item.style.display = 'none';
                item.classList.remove('fade-in');
                item.classList.add('fade-out');
            }
        });
    }

    // 2. Event Listener: Trigger filtering when any checkbox changes
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterPublications);
    });

    // 3. Clear All Filters
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            filterCheckboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            filterPublications();
        });
    }

    // 4. Handle URL parameters for pre-filtering
    function applyUrlFilters() {
        const urlParams = new URLSearchParams(window.location.search);
        const tagFilter = urlParams.get('tag');
        const yearFilter = urlParams.get('year');

        let shouldFilter = false;

        if (tagFilter) {
            const checkbox = document.querySelector(`.pub-filter-checkbox[data-group="tag"][data-filter="${tagFilter}"]`);
            if (checkbox) {
                checkbox.checked = true;
                shouldFilter = true;
            }
        }

        if (yearFilter) {
            const checkbox = document.querySelector(`.pub-filter-checkbox[data-group="year"][data-filter="${yearFilter}"]`);
            if (checkbox) {
                checkbox.checked = true;
                shouldFilter = true;
                // Ensure the year collapse is open if we're filtering by year
                const yearCollapse = document.getElementById('year-collapse');
                if (yearCollapse && !yearCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(yearCollapse, { show: true });
                }
            }
        }

        if (shouldFilter) {
            filterPublications();
        }
    }

    // Run URL filter check on load
    applyUrlFilters();
});
document.addEventListener('DOMContentLoaded', () => {
    // Elementos DOM com verificações de segurança
    const elements = {
        tableBody: document.querySelector('#categoryTable tbody'),
        modal: document.getElementById('modal'),
        detailsModal: document.getElementById('detailsModal'),
        modalTitle: document.getElementById('modalTitle'),
        categoryNameInput: document.getElementById('categoryName'),
        parentCategorySelect: document.getElementById('parentCategory'),
        categoryEnabledCheckbox: document.getElementById('categoryEnabled'),
        saveBtn: document.getElementById('saveCategoryBtn'),
        closeModalBtn: document.getElementById('closeModalBtn'),
        cancelBtn: document.getElementById('cancelBtn'),
        searchInput: document.getElementById('searchInput'),
        searchBtn: document.getElementById('searchBtn'),
        sortBtn: document.getElementById('sortBtn'),
        exportBtn: document.getElementById('exportBtn'),
        resetBtn: document.getElementById('resetBtn'),
        statusFilter: document.getElementById('statusFilter'),
        typeFilter: document.getElementById('typeFilter'),
        itemsPerPageSelect: document.getElementById('itemsPerPage'),
        userWelcome: document.getElementById('userWelcome'),
        userEmail: document.getElementById('userEmail')
    };

    // Verificar elementos críticos
    if (!elements.tableBody || !elements.modal) {
        console.error('Elementos DOM críticos não encontrados');
        showToast('Erro na inicialização da página', 'error');
        return;
    }

    // Variáveis de estado
    let currentCategoryId = null;
    let currentPage = 0;
    let pageSize = parseInt(elements.itemsPerPageSelect?.value) || 10;
    let currentSort = 'name,asc';
    let currentSearch = '';
    let currentStatusFilter = 'all';
    let currentTypeFilter = 'all';
    let totalCategories = 0;
    let totalPages = 0;
    let abortController = null;

    // === INICIALIZAÇÃO ===
    async function init() {
        try {
            await loadUserInfo();
            await loadParentCategories();
            await loadCategories(0);
            setupEventListeners();
            setupModernFeatures();
        } catch (error) {
            console.error('Erro na inicialização:', error);
            showToast('Erro ao carregar dashboard', 'error');
        }
    }

    function setupEventListeners() {
        // Botões principais com verificações
        const addBtn = document.getElementById('addCategoryBtn');
        if (addBtn) addBtn.addEventListener('click', openAddModal);
        if (elements.saveBtn) elements.saveBtn.addEventListener('click', saveCategory);
        if (elements.closeModalBtn) elements.closeModalBtn.addEventListener('click', closeModal);
        if (elements.cancelBtn) elements.cancelBtn.addEventListener('click', closeModal);

        // Busca e filtros
        if (elements.searchBtn) elements.searchBtn.addEventListener('click', performSearch);
        if (elements.searchInput) {
            elements.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') performSearch();
            });
            elements.searchInput.addEventListener('input', debounce(performSearch, 500));
        }

        if (elements.sortBtn) elements.sortBtn.addEventListener('click', toggleSort);
        if (elements.exportBtn) elements.exportBtn.addEventListener('click', exportToCSV);
        if (elements.resetBtn) elements.resetBtn.addEventListener('click', resetCategories);

        // Filtros
        if (elements.statusFilter) elements.statusFilter.addEventListener('change', handleFilterChange);
        if (elements.typeFilter) elements.typeFilter.addEventListener('change', handleFilterChange);
        if (elements.itemsPerPageSelect) elements.itemsPerPageSelect.addEventListener('change', handlePageSizeChange);

        // Eventos da tabela (delegação)
        elements.tableBody.addEventListener('click', handleTableClick);

        // Fechar modais com ESC
        document.addEventListener('keydown', handleKeydown);

        // Fechar modais clicando fora
        if (elements.modal) {
            elements.modal.addEventListener('click', (e) => {
                if (e.target === elements.modal) closeModal();
            });
        }
        if (elements.detailsModal) {
            elements.detailsModal.addEventListener('click', (e) => {
                if (e.target === elements.detailsModal) closeDetailsModal();
            });
        }
    }

    function setupModernFeatures() {
        addSkeletonLoading();
        setupOfflineDetection();

        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(() => console.log('Service Worker registrado'))
                .catch(err => console.log('Service Worker falhou:', err));
        }
    }

    function setupOfflineDetection() {
        window.addEventListener('online', () => {
            showToast('Conexão restaurada', 'success');
            loadCategories(currentPage);
        });

        window.addEventListener('offline', () => {
            showToast('Você está offline', 'error');
        });
    }

    // === CARREGAR INFORMAÇÕES DO USUÁRIO ===
    async function loadUserInfo() {
        try {
            const userInfo = {
                email: 'admin@bluevelvet.com',
                name: 'Administrador',
                role: ''
            };

            if (elements.userWelcome) elements.userWelcome.textContent = `Bem-vindo, ${userInfo.name}`;
            if (elements.userEmail) elements.userEmail.textContent = userInfo.email;

            const userInfoEl = document.getElementById('userInfo');
            if (userInfoEl) userInfoEl.textContent = userInfo.role;

            addUserAvatar(userInfo.email);

        } catch (error) {
            console.error('Error loading user info:', error);
            if (elements.userWelcome) elements.userWelcome.textContent = 'Bem-vindo';
            if (elements.userEmail) elements.userEmail.textContent = 'Usuário';
        }
    }

    function addUserAvatar(email) {
        const headerActions = document.querySelector('.header-actions');
        if (!headerActions) return;

        const avatar = document.createElement('div');
        avatar.className = 'user-avatar';
        avatar.innerHTML = `
            <div class="avatar-circle">
                ${email?.charAt(0)?.toUpperCase() || 'U'}
            </div>
        `;

        const userInfo = document.getElementById('userInfo');
        if (userInfo && userInfo.nextSibling) {
            headerActions.insertBefore(avatar, userInfo.nextSibling);
        } else {
            headerActions.appendChild(avatar);
        }
    }

    // === CARREGAR CATEGORIAS PAI PARA O SELECT ===
    async function loadParentCategories() {
        if (!elements.parentCategorySelect) return;

        try {
            showSelectLoading();

            const { data, error } = await safeFetch('/api/categories/top-level?size=100');
            if (error) throw error;

            const categories = data?.content || data || [];
            renderParentCategories(categories);

        } catch (error) {
            console.error('Error loading parent categories:', error);
            showToast('Erro ao carregar categorias pai', 'error');
        } finally {
            hideSelectLoading();
        }
    }

    function renderParentCategories(categories) {
        if (!elements.parentCategorySelect) return;

        elements.parentCategorySelect.innerHTML = '<option value="">Nenhuma (Categoria Raiz)</option>';

        categories.forEach(category => {
            if (!category?.id) return;
            if (currentCategoryId && category.id == currentCategoryId) return;

            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name || `Categoria #${category.id}`;

            if (!category.enabled) {
                option.textContent += ' (Inativa)';
                option.disabled = true;
            }

            elements.parentCategorySelect.appendChild(option);
        });
    }

    function showSelectLoading() {
        if (!elements.parentCategorySelect) return;
        elements.parentCategorySelect.disabled = true;
        elements.parentCategorySelect.innerHTML = '<option value="">Carregando...</option>';
    }

    function hideSelectLoading() {
        if (!elements.parentCategorySelect) return;
        elements.parentCategorySelect.disabled = false;
    }

    // === CARREGAR CATEGORIAS COM FILTROS ===
    async function loadCategories(page = 0) {
        showTableLoading();

        // Cancelar requisição anterior
        if (abortController) {
            abortController.abort();
        }
        abortController = new AbortController();

        try {
            const url = buildCategoriesUrl(page);
            const { data, error } = await safeFetch(url, {
                signal: abortController.signal
            });

            if (error) throw error;

            renderCategories(data);
            updatePagination(data, page);
            updateDashboardInfo(data);

        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('Requisição cancelada');
                return;
            }
            console.error('Error loading categories:', error);
            showToast('Erro ao carregar categorias', 'error');
            renderEmptyState();
        } finally {
            hideTableLoading();
        }
    }

    function buildCategoriesUrl(page) {
        const params = new URLSearchParams({
            page: page,
            size: pageSize,
            sort: currentSort
        });

        if (currentSearch) {
            params.set('name', currentSearch);
            return `/api/categories/search?${params}`;
        }

        if (currentStatusFilter !== 'all') {
            params.set('status', currentStatusFilter);
        }

        if (currentTypeFilter !== 'all') {
            params.set('type', currentTypeFilter);
        }

        return `/api/categories?${params}`;
    }

    // === RENDERIZAR CATEGORIAS NA TABELA ===
    function renderCategories(data) {
        const categories = data?.content || data || [];
        elements.tableBody.innerHTML = '';

        if (!categories.length) {
            renderEmptyState();
            return;
        }

        categories.forEach((category, index) => {
            if (!category?.id) return;

            const row = createCategoryRow(category, index);
            elements.tableBody.appendChild(row);
        });
    }

    function createCategoryRow(category, index) {
        const row = document.createElement('tr');
        const hierarchyLevel = category.parentId ? 'subcategory' : 'root-category';
        const safeName = escapeHtml(category.name || `Categoria #${category.id}`);

        row.style.animationDelay = `${index * 0.05}s`;
        row.className = 'fade-in-row';

        row.innerHTML = `
            <td>
                <span class="category-id">#${category.id}</span>
            </td>
            <td class="${hierarchyLevel}">
                <div class="category-name-container">
                    ${category.parentId ?
            '<span class="subcategory-indent" title="Subcategoria">↳</span>' :
            '<span class="root-category-indent" title="Categoria Principal">●</span>'
        }
                    <span class="category-name">${safeName}</span>
                    ${!category.enabled ? '<span class="disabled-badge" title="Categoria desativada">Desativada</span>' : ''}
                </div>
            </td>
            <td>
                <span class="status-badge ${category.enabled ? 'status-active' : 'status-inactive'}">
                    ${category.enabled ? 'Ativa' : 'Inativa'}
                </span>
            </td>
            <td>
                <span class="type-badge ${category.parentId ? 'type-subcategory' : 'type-root'}">
                    ${category.parentId ? 'Subcategoria' : 'Categoria Raiz'}
                </span>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn-action btn-view" data-id="${category.id}" title="Ver detalhes">
                        <span class="btn-text">Detalhes</span>
                    </button>
                    <button class="btn-action btn-edit" 
                            data-id="${category.id}" 
                            data-name="${safeName}" 
                            data-enabled="${category.enabled}" 
                            data-parent="${category.parentId || ''}" 
                            title="Editar categoria">
                        <span class="btn-text">Editar</span>
                    </button>
                    <button class="btn-action btn-delete" 
                            data-id="${category.id}" 
                            data-name="${safeName}" 
                            title="Excluir categoria">
                        <span class="btn-text">Excluir</span>
                    </button>
                </div>
            </td>
        `;
        return row;
    }

    function renderEmptyState() {
        elements.tableBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-state">
                    <div class="empty-state-content">
                        <h3>Nenhuma categoria encontrada</h3>
                        <p>${currentSearch ? 'Tente ajustar os termos da busca ou ' : ''}Clique em "Nova Categoria" para começar</p>
                        ${currentSearch || currentStatusFilter !== 'all' || currentTypeFilter !== 'all' ?
            '<button class="btn-primary" id="clearFiltersBtn">Limpar Filtros</button>' : ''
        }
                    </div>
                </td>
            </tr>
        `;

        const clearBtn = document.getElementById('clearFiltersBtn');
        if (clearBtn) clearBtn.addEventListener('click', clearFilters);
    }

    // === ATUALIZAR INFORMAÇÕES DO DASHBOARD ===
    function updateDashboardInfo(data) {
        const categories = data?.content || data || [];
        totalCategories = data?.totalElements || categories.length;
        totalPages = data?.totalPages || 1;
        const pageNumber = data?.number || 0;

        updateElementText('totalCategories', totalCategories);
        updateElementText('currentPageInfo', `${pageNumber + 1}/${totalPages}`);

        const activeCount = categories.filter(cat => cat?.enabled).length;
        updateElementText('activeCount', activeCount);

        const startItem = (pageNumber * pageSize) + (categories.length ? 1 : 0);
        const endItem = Math.min(startItem + categories.length - 1, totalCategories);

        updateElementText('showingStart', startItem);
        updateElementText('showingEnd', endItem);
        updateElementText('totalItems', totalCategories);
    }

    function updateElementText(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = typeof value === 'number' ?
                value.toLocaleString('pt-BR') : String(value);
        }
    }

    // === PAGINAÇÃO ===
    function updatePagination(data, currentPageLocal) {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;

        const totalP = data?.totalPages || 1;
        const pageNumber = data?.number || 0;

        if (totalP <= 1) {
            pagination.innerHTML = '';
            return;
        }

        pagination.innerHTML = '';

        // Botão anterior
        if (!data.first) {
            pagination.appendChild(createPaginationButton('‹',
                () => loadCategories(pageNumber - 1), false, 'pagination-prev'));
        }

        const startPage = Math.max(0, pageNumber - 2);
        const endPage = Math.min(totalP - 1, pageNumber + 2);

        // Primeira página
        if (startPage > 0) {
            pagination.appendChild(createPaginationButton('1', () => loadCategories(0)));
            if (startPage > 1) {
                pagination.appendChild(createPaginationEllipsis());
            }
        }

        // Páginas do meio
        for (let i = startPage; i <= endPage; i++) {
            pagination.appendChild(createPaginationButton(
                String(i + 1),
                () => loadCategories(i),
                i === pageNumber
            ));
        }

        // Última página
        if (endPage < totalP - 1) {
            if (endPage < totalP - 2) {
                pagination.appendChild(createPaginationEllipsis());
            }
            pagination.appendChild(createPaginationButton(
                String(totalP),
                () => loadCategories(totalP - 1)
            ));
        }

        // Botão próximo
        if (!data.last) {
            pagination.appendChild(createPaginationButton('›',
                () => loadCategories(pageNumber + 1), false, 'pagination-next'));
        }
    }

    function createPaginationButton(text, onClick, isActive = false, className = '') {
        const button = document.createElement('button');
        button.textContent = text;
        button.className = `pagination-btn ${isActive ? 'pagination-active' : ''} ${className}`;
        button.onclick = onClick;
        return button;
    }

    function createPaginationEllipsis() {
        const ellipsis = document.createElement('span');
        ellipsis.className = 'pagination-ellipsis';
        ellipsis.textContent = '...';
        return ellipsis;
    }

    // === MODAL - ADICIONAR/EDITAR ===
    function openAddModal() {
        if (!elements.modal || !elements.categoryNameInput) return;

        elements.modalTitle.textContent = 'Nova Categoria';
        elements.categoryNameInput.value = '';
        if (elements.categoryEnabledCheckbox) elements.categoryEnabledCheckbox.checked = true;
        if (elements.parentCategorySelect) elements.parentCategorySelect.value = '';
        currentCategoryId = null;

        clearError('nameError');
        showModal(elements.modal);
    }

    function openEditModal(categoryId, categoryName, enabled, parentId) {
        if (!elements.modal || !elements.categoryNameInput) return;

        elements.modalTitle.textContent = 'Editar Categoria';
        elements.categoryNameInput.value = categoryName || '';
        if (elements.categoryEnabledCheckbox) elements.categoryEnabledCheckbox.checked = Boolean(enabled);
        if (elements.parentCategorySelect) elements.parentCategorySelect.value = parentId || '';
        currentCategoryId = categoryId;

        clearError('nameError');
        showModal(elements.modal);
    }

    function showModal(modal) {
        modal.classList.remove('hidden');
        trapFocus(modal);

        setTimeout(() => {
            if (elements.categoryNameInput) {
                elements.categoryNameInput.focus();
                elements.categoryNameInput.classList.add('input-focus');
            }
        }, 300);
    }

    function closeModal() {
        if (!elements.modal) return;
        elements.modal.classList.add('hidden');
        currentCategoryId = null;
        if (elements.categoryNameInput) {
            elements.categoryNameInput.classList.remove('input-focus', 'input-error');
        }
    }

    // === SALVAR CATEGORIA ===
    async function saveCategory() {
        if (!elements.categoryNameInput) return;

        const name = elements.categoryNameInput.value.trim();
        if (!name) {
            showError('Informe um nome para a categoria.', 'nameError');
            elements.categoryNameInput.classList.add('input-error');
            return;
        }

        showLoading();
        try {
            const categoryData = {
                name: name,
                enabled: elements.categoryEnabledCheckbox ?
                    Boolean(elements.categoryEnabledCheckbox.checked) : true,
                parentId: elements.parentCategorySelect?.value ?
                    parseInt(elements.parentCategorySelect.value) : null
            };

            const method = currentCategoryId ? 'PUT' : 'POST';
            const url = currentCategoryId ?
                `/api/categories/${currentCategoryId}` : '/api/categories';

            const { data, error } = await safeFetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(categoryData)
            });

            if (error) throw error;

            closeModal();
            await loadCategories(currentPage);
            showToast(
                currentCategoryId ? 'Categoria atualizada com sucesso!' : 'Categoria criada com sucesso!',
                'success'
            );

        } catch (error) {
            console.error('Error saving category:', error);
            showError(error.message || 'Erro ao salvar categoria', 'nameError');
            elements.categoryNameInput.classList.add('input-error');
        } finally {
            hideLoading();
        }
    }

    // === MODAL DE DETALHES ===
    async function showCategoryDetails(categoryId) {
        if (!elements.detailsModal) return;

        showLoading();
        try {
            const { data, error } = await safeFetch(`/api/categories/${categoryId}/with-children`);
            if (error) throw error;

            renderCategoryDetails(data);

        } catch (error) {
            console.error('Error loading category details:', error);
            showToast('Erro ao carregar detalhes da categoria', 'error');
        } finally {
            hideLoading();
        }
    }

    function renderCategoryDetails(category) {
        if (!category) return;

        // Informações básicas
        updateDetailElement('detailId', category.id);
        updateDetailElement('detailName', category.name);
        updateDetailElement('detailStatus', category.enabled ? 'Ativa' : 'Inativa');
        updateDetailElement('detailParent', category.parentName || 'Nenhuma (Categoria Raiz)');
        updateDetailElement('detailHasChildren', category.children?.length ? 'Sim' : 'Não');

        const statusEl = document.getElementById('detailStatus');
        if (statusEl) {
            statusEl.className = `detail-value ${category.enabled ? 'status-active' : 'status-inactive'}`;
        }

        // Formatar datas
        updateDetailElement('detailCreated', formatDate(category.createdAt));
        updateDetailElement('detailUpdated', formatDate(category.updatedAt));

        // Subcategorias
        if (category.children?.length) {
            renderSubcategories(category.children);
            showElement('hierarchyVisual');
        } else {
            hideElement('hierarchyVisual');
        }

        showModal(elements.detailsModal);
    }

    function updateDetailElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value ?? '-';
        }
    }

    function showElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'block';
    }

    function hideElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'none';
    }

    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            return new Date(dateString).toLocaleDateString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    }

    function renderSubcategories(children) {
        const subcategoriesList = document.getElementById('subcategoriesList');
        if (!subcategoriesList) return;

        subcategoriesList.innerHTML = '';

        children.forEach(child => {
            if (!child?.id) return;

            const subcategoryItem = document.createElement('div');
            subcategoryItem.className = 'subcategory-item';
            subcategoryItem.innerHTML = `
                <div class="subcategory-info">
                    <span class="subcategory-name">${escapeHtml(child.name || '')}</span>
                    <span class="subcategory-id">#${child.id}</span>
                </div>
                <span class="subcategory-status ${child.enabled ? 'status-active' : 'status-inactive'}">
                    ${child.enabled ? 'Ativa' : 'Inativa'}
                </span>
            `;

            subcategoryItem.addEventListener('click', () => {
                closeDetailsModal();
                setTimeout(() => showCategoryDetails(child.id), 300);
            });

            subcategoriesList.appendChild(subcategoryItem);
        });
    }

    function closeDetailsModal() {
        if (!elements.detailsModal) return;
        elements.detailsModal.classList.add('hidden');
    }

    // === EXCLUIR CATEGORIA ===
    async function deleteCategory(categoryId, categoryName) {
        showConfirmModal(
            'Confirmar Exclusão',
            `Tem certeza que deseja excluir a categoria "<strong>${escapeHtml(categoryName)}</strong>"?<br><small>Esta ação não pode ser desfeita.</small>`,
            async () => {
                showLoading();
                try {
                    const { error } = await safeFetch(`/api/categories/${categoryId}`, {
                        method: 'DELETE'
                    });

                    if (error) throw error;

                    await loadCategories(currentPage);
                    showToast('Categoria excluída com sucesso!', 'success');
                } catch (error) {
                    console.error('Error deleting category:', error);
                    showToast(error.message || 'Erro ao excluir categoria', 'error');
                } finally {
                    hideLoading();
                }
            }
        );
    }

    // === FUNÇÕES DE BUSCA E ORDENAÇÃO ===
    function performSearch() {
        currentSearch = elements.searchInput?.value.trim() || '';
        currentPage = 0;
        loadCategories(currentPage);
    }

    function toggleSort() {
        const sortStates = [
            { sort: 'name,asc', text: 'Ordenar A-Z' },
            { sort: 'name,desc', text: 'Ordenar Z-A' },
            { sort: 'id,asc', text: 'ID Crescente' },
            { sort: 'id,desc', text: 'ID Decrescente' }
        ];

        const currentIndex = sortStates.findIndex(state => state.sort === currentSort);
        const nextIndex = (currentIndex + 1) % sortStates.length;
        const nextState = sortStates[nextIndex];

        currentSort = nextState.sort;
        if (elements.sortBtn) {
            elements.sortBtn.innerHTML = `<span class="btn-text">${nextState.text}</span>`;
        }

        loadCategories(currentPage);
    }

    function handleFilterChange() {
        currentStatusFilter = elements.statusFilter?.value || 'all';
        currentTypeFilter = elements.typeFilter?.value || 'all';
        currentPage = 0;
        loadCategories(currentPage);
    }

    function handlePageSizeChange() {
        pageSize = parseInt(elements.itemsPerPageSelect?.value) || 10;
        currentPage = 0;
        loadCategories(currentPage);
    }

    // === EXPORTAÇÃO ===
    async function exportToCSV() {
        showLoading();
        try {
            const { data, error } = await safeFetch('/api/categories/export');
            if (error) throw error;

            generateCSV(data || []);
            showToast('CSV exportado com sucesso!', 'success');
        } catch (error) {
            console.error('Error exporting categories:', error);
            showToast('Erro ao exportar categorias', 'error');
        } finally {
            hideLoading();
        }
    }

    function generateCSV(categories) {
        if (!Array.isArray(categories)) categories = [];

        const headers = ['ID', 'Nome', 'Status', 'Categoria Pai', 'Data Criação'];
        const rows = categories.map(cat => [
            cat.id || '',
            `"${(cat.name || '').replace(/"/g, '""')}"`,
            cat.enabled ? 'Ativa' : 'Inativa',
            `"${(cat.parentName || '').replace(/"/g, '""')}"`,
            cat.createdAt ? new Date(cat.createdAt).toLocaleDateString('pt-BR') : ''
        ]);

        const csvContent = [headers, ...rows]
            .map(row => row.join(','))
            .join('\n');

        downloadFile(csvContent, `categorias_${getFormattedDate()}.csv`, 'text/csv');
    }

    function downloadFile(content, filename, mimeType) {
        const blob = new Blob(['\uFEFF' + content], { type: `${mimeType};charset=utf-8;` });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');

        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    function getFormattedDate() {
        return new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');
    }

    // === RESET CATEGORIAS ===
    async function resetCategories() {
        showConfirmModal(
            'Reset de Categorias',
            '<strong>ATENÇÃO</strong><br>Isso irá resetar todas as categorias para o estado inicial.<br><small>Esta ação é irreversível e afetará todos os usuários.</small>',
            async () => {
                showLoading();
                try {
                    const { error } = await safeFetch('/api/categories/reset', {
                        method: 'POST'
                    });

                    if (error) throw error;

                    await loadCategories(0);
                    showToast('Categorias resetadas com sucesso!', 'success');
                } catch (error) {
                    console.error('Error resetting categories:', error);
                    showToast('Erro ao resetar categorias', 'error');
                } finally {
                    hideLoading();
                }
            }
        );
    }

    // === MANIPULADOR DE EVENTOS DA TABELA ===
    function handleTableClick(event) {
        const target = event.target.closest('.btn-action');
        if (!target) return;

        const categoryId = target.dataset.id;
        const categoryName = target.dataset.name;

        if (!categoryId) return;

        if (target.classList.contains('btn-view')) {
            showCategoryDetails(categoryId);
        } else if (target.classList.contains('btn-edit')) {
            openEditModal(
                categoryId,
                target.dataset.name,
                target.dataset.enabled === 'true',
                target.dataset.parent
            );
        } else if (target.classList.contains('btn-delete')) {
            deleteCategory(categoryId, categoryName);
        }
    }

    // === MODAL DE CONFIRMAÇÃO ===
    function showConfirmModal(title, message, onConfirm) {
        const confirmModal = document.getElementById('confirmModal');
        const confirmTitle = document.getElementById('confirmTitle');
        const confirmMessage = document.getElementById('confirmMessage');
        const confirmOk = document.getElementById('confirmOk');
        const confirmCancel = document.getElementById('confirmCancel');

        if (!confirmModal || !confirmTitle || !confirmMessage) return;

        confirmTitle.textContent = title;
        confirmMessage.innerHTML = message;

        const cleanUp = () => {
            if (confirmOk) confirmOk.onclick = null;
            if (confirmCancel) confirmCancel.onclick = null;
            confirmModal.classList.add('hidden');
        };

        if (confirmOk) {
            confirmOk.onclick = () => {
                try {
                    onConfirm();
                } catch (error) {
                    console.error('Confirm callback error:', error);
                    showToast('Erro ao executar ação', 'error');
                }
                cleanUp();
            };
        }

        if (confirmCancel) {
            confirmCancel.onclick = cleanUp;
        }

        confirmModal.classList.remove('hidden');
        trapFocus(confirmModal);
    }

    // === UTILITÁRIOS AVANÇADOS ===
    async function safeFetch(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });

            if (!response.ok) {
                let errorMessage = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.message || errorMessage;
                } catch {
                    // Ignora erro de parsing
                }
                return { data: null, error: new Error(errorMessage) };
            }

            const data = await response.json();
            return { data, error: null };
        } catch (error) {
            return { data: null, error };
        }
    }

    function showLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) loadingOverlay.classList.remove('hidden');
    }

    function hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) loadingOverlay.classList.add('hidden');
    }

    function showTableLoading() {
        if (!elements.tableBody) return;

        elements.tableBody.innerHTML = '';
        for (let i = 0; i < pageSize; i++) {
            const row = document.createElement('tr');
            row.className = 'loading-row';
            row.innerHTML = `
                <td><div class="skeleton skeleton-text" style="width:70%"></div></td>
                <td><div class="skeleton skeleton-text" style="width:50%"></div></td>
                <td><div class="skeleton skeleton-badge"></div></td>
                <td><div class="skeleton skeleton-badge"></div></td>
                <td><div class="skeleton skeleton-buttons"></div></td>
            `;
            elements.tableBody.appendChild(row);
        }
    }

    function hideTableLoading() {
        document.querySelectorAll('.loading-row').forEach(row => row.remove());
    }

    function addSkeletonLoading() {
        if (document.getElementById('__skeleton_styles__')) return;

        const style = document.createElement('style');
        style.id = '__skeleton_styles__';
        style.textContent = `
            .skeleton {
                background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                background-size: 200% 100%;
                animation: loading 1.5s infinite;
                border-radius: 4px;
            }
            .skeleton-text { height: 16px; margin: 4px 0; }
            .skeleton-badge { height: 24px; width: 80px; }
            .skeleton-buttons { height: 32px; width: 120px; }
            @keyframes loading {
                0% { background-position: 200% 0; }
                100% { background-position: -200% 0; }
            }
            .fade-in-row {
                animation: fadeInUp 0.3s ease-out forwards;
                opacity: 0;
            }
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(12px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }

    function showToast(message, type = 'info') {
        const existingToast = document.querySelector('.toast');
        if (existingToast) existingToast.remove();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${escapeHtml(message)}</span>
              <button class="toast-close" aria-label="">×</button> 
            </div>
        `;

        Object.assign(toast.style, {
            position: 'fixed',
            right: '20px',
            bottom: '20px',
            zIndex: '10000',
            opacity: '0',
            transform: 'translateY(20px)',
            transition: 'all 0.3s ease'
        });

        document.body.appendChild(toast);

        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => removeToast(toast));
        }

        // Animação de entrada
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });

        // Auto-remover
        setTimeout(() => removeToast(toast), 5000);
    }

    function removeToast(toast) {
        if (toast.parentElement) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function escapeHtml(unsafe) {
        if (typeof unsafe !== 'string') return unsafe === null || unsafe === undefined ? '' : String(unsafe);
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function handleKeydown(event) {
        if (event.key === 'Escape') {
            if (elements.modal && !elements.modal.classList.contains('hidden')) closeModal();
            if (elements.detailsModal && !elements.detailsModal.classList.contains('hidden')) closeDetailsModal();

            const confirmModal = document.getElementById('confirmModal');
            if (confirmModal && !confirmModal.classList.contains('hidden')) {
                confirmModal.classList.add('hidden');
            }
        }
    }

    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleTabKey = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        };

        element.addEventListener('keydown', handleTabKey);
        firstElement.focus();

        // Cleanup function
        return () => element.removeEventListener('keydown', handleTabKey);
    }

    function clearFilters() {
        if (elements.searchInput) elements.searchInput.value = '';
        if (elements.statusFilter) elements.statusFilter.value = 'all';
        if (elements.typeFilter) elements.typeFilter.value = 'all';
        currentSearch = '';
        currentStatusFilter = 'all';
        currentTypeFilter = 'all';
        currentPage = 0;
        loadCategories(currentPage);
    }

    function clearError(elementId) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) errorElement.textContent = '';
    }

    function showError(message, elementId) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) errorElement.textContent = message;
    }

    function closeModal() {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.classList.add('hidden');
            modal.style.display = 'none';
        }
        currentCategoryId = null;

        // Remove classes de erro dos inputs
        const nameInput = document.getElementById('categoryName');
        if (nameInput) {
            nameInput.classList.remove('input-focus', 'input-error');
        }
    }

    function closeDetailsModal() {
        const detailsModal = document.getElementById('detailsModal');
        if (detailsModal) {
            detailsModal.classList.add('hidden');
            detailsModal.style.display = 'none';
        }
    }

// Adicione esta função para fechar modal de confirmação
    function closeConfirmModal() {
        const confirmModal = document.getElementById('confirmModal');
        if (confirmModal) {
            confirmModal.classList.add('hidden');
            confirmModal.style.display = 'none';
        }
    }

// Atualize a função showModal para garantir visibilidade
    function showModal(modal) {
        if (!modal) return;

        modal.classList.remove('hidden');
        modal.style.display = 'flex'; // Importante para modal flex

        // Foca no primeiro elemento input
        setTimeout(() => {
            const firstInput = modal.querySelector('input');
            if (firstInput) {
                firstInput.focus();
                firstInput.classList.add('input-focus');
            }
        }, 100);

        trapFocus(modal);
    }

    function setupEventListeners() {
        // Botões principais com verificações
        const addBtn = document.getElementById('addCategoryBtn');
        if (addBtn) addBtn.addEventListener('click', openAddModal);

        if (elements.saveBtn) elements.saveBtn.addEventListener('click', saveCategory);
        if (elements.closeModalBtn) elements.closeModalBtn.addEventListener('click', closeModal);
        if (elements.cancelBtn) elements.cancelBtn.addEventListener('click', closeModal);

        // Busca e filtros
        if (elements.searchBtn) elements.searchBtn.addEventListener('click', performSearch);
        if (elements.searchInput) {
            elements.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') performSearch();
            });
            elements.searchInput.addEventListener('input', debounce(performSearch, 500));
        }

        if (elements.sortBtn) elements.sortBtn.addEventListener('click', toggleSort);
        if (elements.exportBtn) elements.exportBtn.addEventListener('click', exportToCSV);
        if (elements.resetBtn) elements.resetBtn.addEventListener('click', resetCategories);

        // Filtros
        if (elements.statusFilter) elements.statusFilter.addEventListener('change', handleFilterChange);
        if (elements.typeFilter) elements.typeFilter.addEventListener('change', handleFilterChange);
        if (elements.itemsPerPageSelect) elements.itemsPerPageSelect.addEventListener('change', handlePageSizeChange);

        // Eventos da tabela (delegação)
        if (elements.tableBody) {
            elements.tableBody.addEventListener('click', handleTableClick);
        }

        // Fechar modais com ESC
        document.addEventListener('keydown', handleKeydown);

        // Fechar modais clicando fora - CORREÇÃO APLICADA
        document.addEventListener('click', (e) => {
            // Modal principal
            if (elements.modal && !elements.modal.classList.contains('hidden')) {
                if (e.target === elements.modal) {
                    closeModal();
                }
            }

            // Modal de detalhes
            if (elements.detailsModal && !elements.detailsModal.classList.contains('hidden')) {
                if (e.target === elements.detailsModal) {
                    closeDetailsModal();
                }
            }

            // Modal de confirmação
            const confirmModal = document.getElementById('confirmModal');
            if (confirmModal && !confirmModal.classList.contains('hidden')) {
                if (e.target === confirmModal) {
                    closeConfirmModal();
                }
            }
        });

        // Event listeners específicos para botões de fechar nos modais
        const modalCloseBtns = document.querySelectorAll('.close-btn, [data-close-modal]');
        modalCloseBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const modal = btn.closest('.modal');
                if (modal) {
                    if (modal.id === 'modal') closeModal();
                    else if (modal.id === 'detailsModal') closeDetailsModal();
                    else if (modal.id === 'confirmModal') closeConfirmModal();
                    else modal.classList.add('hidden');
                }
            });
        });
    }

    function handleKeydown(event) {
        if (event.key === 'Escape') {
            // Fecha qualquer modal aberto
            if (elements.modal && !elements.modal.classList.contains('hidden')) {
                closeModal();
                event.preventDefault();
            } else if (elements.detailsModal && !elements.detailsModal.classList.contains('hidden')) {
                closeDetailsModal();
                event.preventDefault();
            } else {
                const confirmModal = document.getElementById('confirmModal');
                if (confirmModal && !confirmModal.classList.contains('hidden')) {
                    closeConfirmModal();
                    event.preventDefault();
                }
            }
        }
    }

    function closeModal() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.classList.add('hidden');
            modal.style.display = 'none';
        });
        currentCategoryId = null;

        // Remove classes de erro
        const nameInput = document.getElementById('categoryName');
        if (nameInput) {
            nameInput.classList.remove('input-focus', 'input-error');
        }
    }

// E garanta que o event listener está correto:
    if (elements.closeModalBtn) {
        elements.closeModalBtn.addEventListener('click', closeModal);
    }
    if (elements.cancelBtn) {
        elements.cancelBtn.addEventListener('click', closeModal);
    }

    function handleFilterChange() {
        console.log('Filtro alterado'); // Para debug

        currentStatusFilter = elements.statusFilter?.value || 'all';
        currentTypeFilter = elements.typeFilter?.value || 'all';
        currentPage = 0;

        console.log('Status:', currentStatusFilter, 'Tipo:', currentTypeFilter); // Debug

        loadCategories(currentPage);
    }

// E garanta que os event listeners estão corretos:
    if (elements.statusFilter) {
        elements.statusFilter.addEventListener('change', handleFilterChange);
    }
    if (elements.typeFilter) {
        elements.typeFilter.addEventListener('change', handleFilterChange);
    }
    if (elements.itemsPerPageSelect) {
        elements.itemsPerPageSelect.addEventListener('change', handlePageSizeChange);
    }

    function handlePageSizeChange() {
        pageSize = parseInt(elements.itemsPerPageSelect?.value) || 10;
        currentPage = 0;
        console.log('Itens por página:', pageSize); // Debug
        loadCategories(currentPage);
    }

    async function loadCategories(page = 0) {
        console.log('Carregando categorias...', {
            page,
            pageSize,
            search: currentSearch,
            status: currentStatusFilter,
            type: currentTypeFilter
        });

        showTableLoading();

        try {
            const url = buildCategoriesUrl(page);
            console.log('URL da requisição:', url); // Debug

            const { data, error } = await safeFetch(url);

            if (error) {
                console.error('Erro na requisição:', error);
                throw error;
            }

            console.log('Dados recebidos:', data); // Debug

            // Se não há dados, simule alguns para teste
            if (!data || (!data.content && !Array.isArray(data))) {
                console.log('Sem dados da API, usando dados de teste');
                renderTestData();
                return;
            }

            renderCategories(data);
            updatePagination(data, page);
            updateDashboardInfo(data);

        } catch (error) {
            console.error('Error loading categories:', error);

            // Em caso de erro, mostra dados de teste
            renderTestData();
            showToast('Erro ao carregar categorias. Mostrando dados de exemplo.', 'warning');
        } finally {
            hideTableLoading();
        }
    }

// Função para mostrar dados de teste
    function renderTestData() {
        const testData = {
            content: [
                {
                    id: 1,
                    name: "Eletrônicos",
                    enabled: true,
                    parentId: null,
                    createdAt: "2024-01-15T10:30:00Z"
                },
                {
                    id: 2,
                    name: "Smartphones",
                    enabled: true,
                    parentId: 1,
                    createdAt: "2024-01-16T14:20:00Z"
                },
                {
                    id: 3,
                    name: "Roupas",
                    enabled: true,
                    parentId: null,
                    createdAt: "2024-01-17T09:15:00Z"
                },
                {
                    id: 4,
                    name: "Camisetas",
                    enabled: false,
                    parentId: 3,
                    createdAt: "2024-01-18T11:45:00Z"
                }
            ],
            totalElements: 4,
            totalPages: 1,
            number: 0
        };

        renderCategories(testData);
        updatePagination(testData, 0);
        updateDashboardInfo(testData);
    }

    function buildCategoriesUrl(page) {
        // Para teste, use dados mockados se a API não estiver respondendo
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('Modo desenvolvimento - usando URL base');
        }

        const params = new URLSearchParams({
            page: page,
            size: pageSize,
            sort: currentSort
        });

        console.log('Parâmetros atuais:', {
            currentSearch,
            currentStatusFilter,
            currentTypeFilter
        });

        // Busca por texto
        if (currentSearch) {
            params.set('name', currentSearch);
            return `/api/categories/search?${params}`;
        }

        // Filtro por status
        if (currentStatusFilter !== 'all') {
            params.set('enabled', currentStatusFilter === 'active' ? 'true' : 'false');
        }

        // Filtro por tipo
        if (currentTypeFilter !== 'all') {
            if (currentTypeFilter === 'root') {
                params.set('parentId', 'null'); // Categorias raiz
            } else if (currentTypeFilter === 'subcategory') {
                params.set('parentId', 'notNull'); // Subcategorias
            }
        }

        const finalUrl = `/api/categories?${params}`;
        console.log('URL final:', finalUrl);
        return finalUrl;
    }

    // No final do DOMContentLoaded, adicione:
    console.log('=== DEBUG MODAL STATUS ===');
    console.log('Modal element:', document.getElementById('modal'));
    console.log('Details modal:', document.getElementById('detailsModal'));
    console.log('Confirm modal:', document.getElementById('confirmModal'));

// Verifica event listeners
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('close-btn') || e.target.closest('.close-btn')) {
            console.log('Close button clicked:', e.target);
        }
    });

    // Expor funções globais
    window.clearFilters = clearFilters;

    // INICIAR APLICAÇÃO
    init();
});


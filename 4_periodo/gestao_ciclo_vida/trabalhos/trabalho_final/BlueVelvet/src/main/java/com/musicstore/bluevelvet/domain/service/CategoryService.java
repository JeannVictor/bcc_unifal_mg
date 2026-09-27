package com.musicstore.bluevelvet.domain.service;

import com.musicstore.bluevelvet.api.request.CategoryRequest;
import com.musicstore.bluevelvet.api.response.CategoryResponse;
import com.musicstore.bluevelvet.domain.converter.CategoryConverter;
import com.musicstore.bluevelvet.domain.exception.CategoryHasChildrenException;
import com.musicstore.bluevelvet.domain.exception.CategoryNotFoundException;
import com.musicstore.bluevelvet.domain.exception.DuplicateCategoryNameException;
import com.musicstore.bluevelvet.infrastructure.entity.Category;
import com.musicstore.bluevelvet.infrastructure.repository.CategoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Log4j2
@Service
@RequiredArgsConstructor
public class CategoryService {

    private final CategoryRepository categoryRepository;
    // private final ImageStorageService imageStorageService; // TODO: Implementar depois

    // =========================================================================
    // US-2032: Access the Category Management Dashboard
    // =========================================================================

    public CategoryResponse findById(Long id) {
        log.debug("Finding Category with id: {}", id);

        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Category with id {} not found", id);
                    return new CategoryNotFoundException(
                            "Unable to find a category with id %d".formatted(id)
                    );
                });

        return CategoryConverter.toResponse(category);
    }

    public Page<CategoryResponse> findAll(Pageable pageable) {
        log.debug("Finding all categories with pageable: {}", pageable);
        return categoryRepository.findAll(pageable)
                .map(CategoryConverter::toResponse);
    }

    /**
     * US-2032: Reset categories to initial state (10 initial categories)
     * Útil para testes
     */
    @Transactional
    public void resetToInitialState() {
        log.debug("Resetting categories to initial state");

        // Deletar todas as categorias
        categoryRepository.deleteAll();
        log.info("All categories deleted");

        // TODO: Chamar script de dados iniciais
        // categoryDataLoader.loadInitialCategories();

        log.info("Categories reset to initial state (10 categories)");
    }

    // =========================================================================
    // US-1306: Create category of products
    // =========================================================================

    @Transactional
    public CategoryResponse createCategory(CategoryRequest request) {
        log.debug("Creating new category: {}", request.getName());

        if (categoryRepository.existsByName(request.getName())) {
            log.error("Category name already exists: {}", request.getName());
            throw new DuplicateCategoryNameException(
                    "Category name already exists: " + request.getName()
            );
        }

        Category category = CategoryConverter.convertToCategory(request);

        if (request.getParentId() != null) {
            Category parent = categoryRepository.findById(request.getParentId())
                    .orElseThrow(() -> {
                        log.error("Parent category not found: {}", request.getParentId());
                        return new CategoryNotFoundException(
                                "Parent category not found with id: " + request.getParentId()
                        );
                    });
            category.setParent(parent);
        }

        // TODO: Upload de imagem (implementar depois) - US-1306
        // if (request.getImage() != null) {
        //     String imagePath = imageStorageService.saveImage(request.getImage());
        //     category.setImage(imagePath);
        // }

        Category savedCategory = categoryRepository.save(category);
        log.info("Category created with id: {}", savedCategory.getId());

        return CategoryConverter.toResponse(savedCategory);
    }

    // =========================================================================
    // US-1307: Edit category of products
    // =========================================================================

    @Transactional
    public CategoryResponse updateCategory(Long id, CategoryRequest request) {
        log.debug("Updating category with id: {}", id);

        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Category not found: {}", id);
                    return new CategoryNotFoundException(
                            "Category not found with id: " + id
                    );
                });

        if (!category.getName().equals(request.getName())
                && categoryRepository.existsByName(request.getName())) {
            log.error("Category name already exists: {}", request.getName());
            throw new DuplicateCategoryNameException(
                    "Category name already exists: " + request.getName()
            );
        }

        category.setName(request.getName());
        category.setEnabled(request.getEnabled());

        if (request.getParentId() != null) {
            Category parent = categoryRepository.findById(request.getParentId())
                    .orElseThrow(() -> {
                        log.error("Parent category not found: {}", request.getParentId());
                        return new CategoryNotFoundException(
                                "Parent category not found: " + request.getParentId()
                        );
                    });
            category.setParent(parent);
        } else {
            category.setParent(null); // Tornar root category
        }

        // TODO: Tratamento de imagem (US-1307)
        // if (request.getImage() != null) {
        //     // Deletar imagem antiga se existir
        //     if (category.getImage() != null) {
        //         imageStorageService.deleteImage(category.getImage());
        //     }
        //     // Salvar nova imagem
        //     String newImagePath = imageStorageService.saveImage(request.getImage());
        //     category.setImage(newImagePath);
        // }

        Category saved = categoryRepository.save(category);
        log.info("Category updated with id: {}", saved.getId());

        return CategoryConverter.toResponse(saved);
    }

    // =========================================================================
    // US-0904: Delete category of products
    // =========================================================================

    /**
     * US-0904: Delete category
     * CRÍTICO: Só pode deletar se não tiver filhos!
     */
    @Transactional
    public void deleteById(Long id) {
        log.debug("Attempting to delete category: {}", id);

        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Category not found: {}", id);
                    return new CategoryNotFoundException(
                            "Category not found with id: " + id
                    );
                });

        // ⚠️ US-0904: Validação crítica - não pode ter filhos
        if (categoryRepository.existsByParentId(id)) {
            log.error("Cannot delete category {} - has children", id);
            throw new CategoryHasChildrenException(
                    "Cannot delete category with children. Remove children first."
            );
        }

        // TODO: Deletar imagem (implementar depois) - US-0904
        // if (category.getImage() != null) {
        //     imageStorageService.deleteImage(category.getImage());
        // }

        categoryRepository.deleteById(id);
        log.info("Category {} deleted successfully", id);
    }

    // =========================================================================
    // US-0907: List categories of products
    // =========================================================================

    /**
     * US-0907: List top-level categories (root categories only)
     */
    public Page<CategoryResponse> findTopLevelCategories(Pageable pageable) {
        log.debug("Finding top-level categories (no parent)");
        return categoryRepository.findByParentIsNull(pageable)
                .map(CategoryConverter::toResponse);
    }

    /**
     * US-0907: List top-level categories WITH their direct children
     */
    public Page<CategoryResponse> findTopLevelWithChildren(Pageable pageable) {
        log.debug("Finding top-level categories with children");
        return categoryRepository.findByParentIsNull(pageable)
                .map(CategoryConverter::toResponseWithChildren);
    }

    /**
     * US-0907: Get category by ID with its children (1 level)
     */
    public CategoryResponse findByIdWithChildren(Long id) {
        log.debug("Finding category with children, id: {}", id);

        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Category not found: {}", id);
                    return new CategoryNotFoundException(
                            "Category not found with id: " + id
                    );
                });

        return CategoryConverter.toResponseWithChildren(category);
    }

    /**
     * US-0907: Get subcategories of a parent category
     */
    public List<CategoryResponse> findSubcategories(Long parentId) {
        log.debug("Finding subcategories of category: {}", parentId);

        if (!categoryRepository.existsById(parentId)) {
            log.error("Parent category not found: {}", parentId);
            throw new CategoryNotFoundException(
                    "Parent category not found with id: " + parentId
            );
        }

        return categoryRepository.findByParentId(parentId).stream()
                .map(CategoryConverter::toResponse)
                .toList();
    }

    // =========================================================================
    // US-0914: Filter category of products
    // =========================================================================

    /**
     * US-0914: Search categories by name (filter)
     */
    public Page<CategoryResponse> searchByName(String name, Pageable pageable) {
        log.debug("Searching categories by name: {}", name);
        return categoryRepository.findByNameContainingIgnoreCase(name, pageable)
                .map(CategoryConverter::toResponse);
    }

    // =========================================================================
    // US-0913: Sort category of products
    // =========================================================================

    public Page<CategoryResponse> findAllSorted(Pageable pageable, String sortBy, String direction) {
        log.debug("Finding all categories sorted by {} {}", sortBy, direction);

        Sort.Direction sortDirection = Sort.Direction.fromString(direction);
        Pageable sortedPageable = PageRequest.of(
                pageable.getPageNumber(),
                pageable.getPageSize(),
                Sort.by(sortDirection, sortBy)
        );

        return categoryRepository.findAll(sortedPageable)
                .map(CategoryConverter::toResponse);
    }

    // =========================================================================
    // US-2100: List products within a category for the online shopper
    // =========================================================================

    public Page<CategoryResponse> findAllEnabled(Pageable pageable) {
        log.debug("Finding all enabled categories");
        return categoryRepository.findByEnabledTrue(pageable)
                .map(CategoryConverter::toResponse);
    }

    /**
     * US-2100: List enabled categories for online shoppers
     */
    public List<CategoryResponse> findEnabledCategoriesForShopper() {
        log.debug("Finding enabled categories for shopper");
        return categoryRepository.findByEnabledTrueOrderByNameAsc().stream()
                .map(CategoryConverter::toResponse)
                .toList();
    }

    /**
     * US-2100: List enabled categories with subcategories (hierarchical)
     */
    public List<CategoryResponse> findEnabledCategoriesWithChildren() {
        log.debug("Finding enabled categories with children for shopper");

        // Buscar apenas categorias raiz habilitadas
        List<Category> rootCategories = categoryRepository
                .findByParentIsNullAndEnabledTrue();

        return rootCategories.stream()
                .map(CategoryConverter::toResponseWithChildren)
                .toList();
    }

    // =========================================================================
    // US-0916: Export category of products
    // =========================================================================

    /**
     * US-0916: Export categories to CSV
     * Retorna List para o controller processar em CSV
     */
    public List<CategoryResponse> getAllCategoriesForExport() {
        log.debug("Getting all categories for CSV export");

        // Buscar todas ordenadas por nome
        List<Category> categories = categoryRepository.findAllByOrderByNameAsc();

        return categories.stream()
                .map(CategoryConverter::toResponse)
                .toList();
    }

    // =========================================================================
    //  (Não são User Stories específicos)
    // =========================================================================

    public CategoryResponse findByName(String name) {
        log.debug("Finding Category with name: {}", name);

        Category category = categoryRepository.findByName(name)
                .orElseThrow(() -> {
                    log.error("Category with name {} not found", name);
                    return new CategoryNotFoundException(
                            "Unable to find a category with name %s".formatted(name)
                    );
                });

        return CategoryConverter.toResponse(category);
    }

    public boolean hasChildren(Long categoryId) {
        return categoryRepository.existsByParentId(categoryId);
    }

    public boolean existsByName(String name) {
        return categoryRepository.existsByName(name);
    }
}
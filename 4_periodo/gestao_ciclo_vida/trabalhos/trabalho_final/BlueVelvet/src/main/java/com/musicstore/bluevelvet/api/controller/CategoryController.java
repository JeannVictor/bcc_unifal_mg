package com.musicstore.bluevelvet.api.controller;

import com.musicstore.bluevelvet.api.request.CategoryRequest;
import com.musicstore.bluevelvet.api.response.CategoryResponse;
import com.musicstore.bluevelvet.domain.service.CategoryService;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Log4j2
@RestController
@RequestMapping("/api/categories")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class CategoryController {

    private final CategoryService categoryService;

    // =========================================================================
    // US-2032: Access the Category Management Dashboard
    // =========================================================================

    @Operation(summary = "Fetch a category by id", description = "Fetch a category from the Blue Velvet Music Store (US-2032)")
    @GetMapping("/{id}")
    public ResponseEntity<CategoryResponse> getById(@PathVariable Long id) {
        log.info("GET /api/categories/{}", id);
        CategoryResponse category = categoryService.findById(id);
        return ResponseEntity.ok(category);
    }

    @GetMapping
    @Operation(summary = "Get all categories", description = "Get all categories from the Blue Velvet Music Store (US-2032)")
    public ResponseEntity<Page<CategoryResponse>> getAll(@PageableDefault(size = 10, sort = "name", direction = Sort.Direction.ASC) Pageable pageable) {
        log.info("GET /api/categories - Page: {}, Size: {}",
                pageable.getPageNumber(), pageable.getPageSize());
        Page<CategoryResponse> categories = categoryService.findAll(pageable);
        return ResponseEntity.ok(categories);
    }

    /**
     * Reseta categorias para estado inicial (US-2032)
     * ATENÇÃO: Use apenas para testes
     * Ela provavelmente será removida antes de terminarmos o projeto
     */
    @PostMapping("/reset")
    @Operation(summary = "Reset all categories to initial state", description = "Reset all categories in the database to their initial state (US-2032). ")
    public ResponseEntity<Void> reset() {
        log.warn("POST /api/categories/reset - Resetting all categories!");
        categoryService.resetToInitialState();
        return ResponseEntity.ok().build();
    }

    // =========================================================================
    // US-1306: Create category of products
    // =========================================================================

    @PostMapping
    @Operation(summary = "Create a category by id", description = "Create a category from the Blue Velvet Music Store (US-1306)")
    public ResponseEntity<CategoryResponse> create(@Valid @RequestBody CategoryRequest request) {
        log.info("POST /api/categories - Creating: {}", request.getName());
        CategoryResponse created = categoryService.createCategory(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    // =========================================================================
    // US-1307: Edit category of products
    // =========================================================================

    @PutMapping("/{id}")
    @Operation(summary = "Update a category by id", description = "Update a category from the Blue Velvet Music Store (US-1307)")
    public ResponseEntity<CategoryResponse> update(@PathVariable Long id, @Valid @RequestBody CategoryRequest request) {
        log.info("PUT /api/categories/{} - Updating", id);
        CategoryResponse updated = categoryService.updateCategory(id, request);
        return ResponseEntity.ok(updated);
    }

    // =========================================================================
    // US-0904: Delete category of products
    // =========================================================================

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a category by id", description = "Delete a category(without children) from the Blue Velvet Music Store (US-0904)")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/categories/{}", id);
        categoryService.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // =========================================================================
    // US-0907: List categories of products
    // =========================================================================

    @GetMapping("/top-level")
    @Operation(summary = "List top-level categories", description = "Retrieve all categories that do not have a parent (root categories) from the Blue Velvet Music Store (US-0907)")
    public ResponseEntity<Page<CategoryResponse>> getTopLevel(
            @PageableDefault(size = 5, sort = "name") Pageable pageable
    ) {
        log.info("GET /api/categories/top-level");
        Page<CategoryResponse> topLevel = categoryService.findTopLevelCategories(pageable);
        return ResponseEntity.ok(topLevel);
    }

    @GetMapping("/hierarchy")
    @Operation(summary = "List hierarchical categories", description = "Retrieve all top-level (root) categories along with their direct child categories from the Blue Velvet Music Store (US-0907)")
    public ResponseEntity<Page<CategoryResponse>> getHierarchy(
            @PageableDefault(size = 5, sort = "name") Pageable pageable
    ) {
        log.info("GET /api/categories/hierarchy");
        Page<CategoryResponse> hierarchy = categoryService.findTopLevelWithChildren(pageable);
        return ResponseEntity.ok(hierarchy);
    }

    @GetMapping("/{id}/with-children")
    @Operation(summary = "Fetch category with children", description = "Retrieve a specific category by its ID, including its direct child categories (US-0907)")
    public ResponseEntity<CategoryResponse> getByIdWithChildren(@PathVariable Long id) {
        log.info("GET /api/categories/{}/with-children", id);
        CategoryResponse category = categoryService.findByIdWithChildren(id);
        return ResponseEntity.ok(category);
    }

    @GetMapping("/{id}/subcategories")
    @Operation(summary = "List subcategories of a category", description = "Retrieve all subcategories belonging to the specified parent category ID (US-0907)")
    public ResponseEntity<List<CategoryResponse>> getSubcategories(@PathVariable Long id) {
        log.info("GET /api/categories/{}/subcategories", id);
        List<CategoryResponse> subcategories = categoryService.findSubcategories(id);
        return ResponseEntity.ok(subcategories);
    }

    // =========================================================================
    // US-0914: Filter category of products
    // =========================================================================

    @GetMapping("/search")
    @Operation(summary = "Search categories by name", description = "Search for categories whose names contain the specified text (case-insensitive) (US-0914)")
    public ResponseEntity<Page<CategoryResponse>> search(
            @RequestParam String name,
            @PageableDefault(size = 10, sort = "name") Pageable pageable
    ) {
        log.info("GET /api/categories/search?name={}", name);
        Page<CategoryResponse> results = categoryService.searchByName(name, pageable);
        return ResponseEntity.ok(results);
    }

    // =========================================================================
    // US-0913: Sort category of products
    // =========================================================================

    @GetMapping("/sorted")
    @Operation(summary = "List categories with custom sorting", description = "Retrieve all categories using custom sorting options (US-0913). "
            + "You can specify the sorting field and direction (ASC or DESC). ")
    public ResponseEntity<Page<CategoryResponse>> getSorted(
            @RequestParam(defaultValue = "name") String sortBy,
            @RequestParam(defaultValue = "ASC") String direction,
            @PageableDefault(size = 10) Pageable pageable
    ) {
        log.info("GET /api/categories/sorted?sortBy={}&direction={}", sortBy, direction);
        Page<CategoryResponse> sorted = categoryService.findAllSorted(pageable, sortBy, direction);
        return ResponseEntity.ok(sorted);
    }

    // =========================================================================
    // US-2100: List products within a category for the online shopper
    // =========================================================================

    @GetMapping("/enabled")
    @Operation(summary = "List enabled categories", description = "Retrieve only categories that are currently enabled (active) in the Blue Velvet Music Store (US-2100)")
    public ResponseEntity<Page<CategoryResponse>> getEnabled(
            @PageableDefault(size = 10, sort = "name") Pageable pageable
    ) {
        log.info("GET /api/categories/enabled");
        Page<CategoryResponse> enabled = categoryService.findAllEnabled(pageable);
        return ResponseEntity.ok(enabled);
    }

    @GetMapping("/public")
    @Operation(summary = "List enabled categories for shoppers", description = "Retrieve all enabled (active) categories available to shoppers (US-2100)")
    public ResponseEntity<List<CategoryResponse>> getForShopper() {
        log.info("GET /api/categories/public");
        List<CategoryResponse> categories = categoryService.findEnabledCategoriesForShopper();
        return ResponseEntity.ok(categories);
    }

    @GetMapping("/public/hierarchy")
    @Operation(summary = "List enabled categories with subcategories for shoppers", description = "Retrieve enabled categories along with their direct subcategories (US-2100)")
    public ResponseEntity<List<CategoryResponse>> getForShopperWithChildren() {
        log.info("GET /api/categories/public/hierarchy");
        List<CategoryResponse> categories = categoryService.findEnabledCategoriesWithChildren();
        return ResponseEntity.ok(categories);
    }

    // =========================================================================
    // US-0916: Export category of products
    // =========================================================================
    // TODO: Converter para CSV e retornar como arquivo
    // Por enquanto retorna JSON

    @GetMapping("/export")
    @Operation(summary = "Export all categories in CSV format", description = "Export all categories (including their hierarchy and enabled status) into a CSV file (US-0916). " + "The current implementation returns JSON; ")
    public ResponseEntity<List<CategoryResponse>> export() {
        log.info("GET /api/categories/export");
        List<CategoryResponse> categories = categoryService.getAllCategoriesForExport();


        return ResponseEntity.ok(categories);
    }

    // =========================================================================
    // ENDPOINTS DE VALIDAÇÃO E UTILITÁRIOS (Não são User Stories específicos)
    // =========================================================================

    @GetMapping("/{id}/has-children")
    @Operation(summary = "Check if a category has subcategories", description = "Verify whether a given category (by its ID) has one or more direct child categories")
    public ResponseEntity<Boolean> hasChildren(@PathVariable Long id) {
        log.info("GET /api/categories/{}/has-children", id);
        boolean hasChildren = categoryService.hasChildren(id);
        return ResponseEntity.ok(hasChildren);
    }

    @GetMapping("/exists")
    @Operation(summary = "Check if a category name already exists", description = "Verify whether a category with the given name already exists in the database")
    public ResponseEntity<Boolean> existsByName(@RequestParam String name) {
        log.info("GET /api/categories/exists?name={}", name);
        boolean exists = categoryService.existsByName(name);
        return ResponseEntity.ok(exists);
    }
}
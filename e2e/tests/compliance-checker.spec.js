const { test, expect } = require('@playwright/test');

test.describe('Compliance Checker E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the home page before each test
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test.describe('Page Load and Navigation', () => {
    test('should load the compliance checker page', async ({ page }) => {
      // Check that the page loads successfully
      await expect(page).toHaveTitle(/RegReportRAG/);
      
      // Check that main components are visible
      await expect(page.locator('h1')).toBeVisible();
      await expect(page.locator('form')).toBeVisible();
    });

    test('should display navigation menu', async ({ page }) => {
      // Check navigation links
      await expect(page.locator('nav')).toBeVisible();
      await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
      await expect(page.getByRole('link', { name: 'Documents' })).toBeVisible();
      await expect(page.getByRole('link', { name: 'How It Works' })).toBeVisible();
    });

    test('should navigate to documents page', async ({ page }) => {
      await page.getByRole('link', { name: 'Documents' }).click();
      await page.waitForURL('**/documents');
      
      // Check that we're on the documents page
      await expect(page.locator('h1')).toContainText('Document Status');
    });

    test('should navigate to how-it-works page', async ({ page }) => {
      await page.getByRole('link', { name: 'How It Works' }).click();
      await page.waitForURL('**/how-it-works');
      
      // Check that we're on the how-it-works page
      await expect(page.locator('h1')).toContainText('How It Works');
    });
  });

  test.describe('Compliance Check Form', () => {
    test('should display form fields', async ({ page }) => {
      // Check that form fields are present
      await expect(page.locator('label[for="concern"]')).toBeVisible();
      await expect(page.locator('textarea[name="concern"]')).toBeVisible();
      
      await expect(page.locator('label[for="context"]')).toBeVisible();
      await expect(page.locator('textarea[name="context"]')).toBeVisible();
      
      // Check submit button
      await expect(page.getByRole('button', { name: /check compliance/i })).toBeVisible();
    });

    test('should validate required fields', async ({ page }) => {
      // Try to submit empty form
      await page.getByRole('button', { name: /check compliance/i }).click();
      
      // Should show validation errors
      await expect(page.locator('.error-message')).toBeVisible();
    });

    test('should accept valid input', async ({ page }) => {
      // Fill in valid form data
      await page.locator('textarea[name="concern"]').fill('Data privacy compliance for customer information');
      await page.locator('textarea[name="context"]').fill('Processing customer data for financial services');
      
      // Check that form accepts the input
      await expect(page.locator('textarea[name="concern"]')).toHaveValue('Data privacy compliance for customer information');
      await expect(page.locator('textarea[name="context"]')).toHaveValue('Processing customer data for financial services');
    });
  });

  test.describe('Compliance Check API Integration', () => {
    test('should submit compliance check successfully', async ({ page }) => {
      // Mock API response
      await page.route('**/api/v1/compliance/check', async route => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'compliant',
            confidence: 0.85,
            explanation: 'Based on regulatory guidelines, this appears to be compliant.',
            relevant_sections: ['Section 2.1', 'Section 3.4'],
            recommendations: ['Ensure proper documentation', 'Maintain audit trail']
          })
        });
      });

      // Fill and submit form
      await page.locator('textarea[name="concern"]').fill('Data privacy compliance');
      await page.locator('textarea[name="context"]').fill('Customer data processing');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Wait for response and check results
      await expect(page.locator('.compliance-result')).toBeVisible();
      await expect(page.locator('.compliance-result')).toContainText('compliant');
      await expect(page.locator('.compliance-result')).toContainText('85%');
    });

    test('should handle API errors gracefully', async ({ page }) => {
      // Mock API error
      await page.route('**/api/v1/compliance/check', async route => {
        await route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({
            detail: 'Internal server error'
          })
        });
      });

      // Fill and submit form
      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Should show error message
      await expect(page.locator('.error-message')).toBeVisible();
      await expect(page.locator('.error-message')).toContainText('error');
    });

    test('should show loading state during API call', async ({ page }) => {
      // Mock slow API response
      await page.route('**/api/v1/compliance/check', async route => {
        await new Promise(resolve => setTimeout(resolve, 2000));
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'compliant',
            confidence: 0.85,
            explanation: 'Test explanation',
            relevant_sections: ['Section 1'],
            recommendations: ['Test recommendation']
          })
        });
      });

      // Fill and submit form
      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Should show loading indicator
      await expect(page.locator('.loading-spinner')).toBeVisible();
      
      // Wait for response
      await expect(page.locator('.compliance-result')).toBeVisible();
    });
  });

  test.describe('Compliance Results Display', () => {
    test('should display compliance status correctly', async ({ page }) => {
      // Mock compliant response
      await page.route('**/api/v1/compliance/check', async route => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'compliant',
            confidence: 0.92,
            explanation: 'This is compliant with regulations.',
            relevant_sections: ['Section 1.1', 'Section 2.3'],
            recommendations: ['Continue current practices', 'Monitor for changes']
          })
        });
      });

      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Check status display
      await expect(page.locator('.status-compliant')).toBeVisible();
      await expect(page.locator('.confidence-score')).toContainText('92%');
      await expect(page.locator('.explanation')).toContainText('This is compliant with regulations.');
    });

    test('should display non-compliant status correctly', async ({ page }) => {
      // Mock non-compliant response
      await page.route('**/api/v1/compliance/check', async route => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'non-compliant',
            confidence: 0.78,
            explanation: 'This does not meet regulatory requirements.',
            relevant_sections: ['Section 3.1'],
            recommendations: ['Implement required controls', 'Update procedures']
          })
        });
      });

      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Check status display
      await expect(page.locator('.status-non-compliant')).toBeVisible();
      await expect(page.locator('.confidence-score')).toContainText('78%');
      await expect(page.locator('.explanation')).toContainText('does not meet regulatory requirements');
    });

    test('should display relevant sections and recommendations', async ({ page }) => {
      // Mock response with sections and recommendations
      await page.route('**/api/v1/compliance/check', async route => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'compliant',
            confidence: 0.85,
            explanation: 'Test explanation',
            relevant_sections: ['Section 1.1', 'Section 2.3', 'Section 4.2'],
            recommendations: ['Implement encryption', 'Set up monitoring', 'Train staff']
          })
        });
      });

      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      await page.getByRole('button', { name: /check compliance/i }).click();

      // Check sections and recommendations
      await expect(page.locator('.relevant-sections')).toBeVisible();
      await expect(page.locator('.recommendations')).toBeVisible();
      
      // Check that all sections are displayed
      await expect(page.locator('.relevant-sections')).toContainText('Section 1.1');
      await expect(page.locator('.relevant-sections')).toContainText('Section 2.3');
      await expect(page.locator('.relevant-sections')).toContainText('Section 4.2');
      
      // Check that all recommendations are displayed
      await expect(page.locator('.recommendations')).toContainText('Implement encryption');
      await expect(page.locator('.recommendations')).toContainText('Set up monitoring');
      await expect(page.locator('.recommendations')).toContainText('Train staff');
    });
  });

  test.describe('User Experience', () => {
    test('should provide clear feedback for form validation', async ({ page }) => {
      // Try to submit without filling required fields
      await page.getByRole('button', { name: /check compliance/i }).click();
      
      // Should show validation messages
      await expect(page.locator('.validation-error')).toBeVisible();
      await expect(page.locator('.validation-error')).toContainText('required');
    });

    test('should allow form reset', async ({ page }) => {
      // Fill form
      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      
      // Reset form
      await page.getByRole('button', { name: /reset/i }).click();
      
      // Check that fields are cleared
      await expect(page.locator('textarea[name="concern"]')).toHaveValue('');
      await expect(page.locator('textarea[name="context"]')).toHaveValue('');
    });

    test('should maintain form state during navigation', async ({ page }) => {
      // Fill form
      await page.locator('textarea[name="concern"]').fill('Test concern');
      await page.locator('textarea[name="context"]').fill('Test context');
      
      // Navigate away and back
      await page.getByRole('link', { name: 'Documents' }).click();
      await page.waitForURL('**/documents');
      await page.getByRole('link', { name: 'Home' }).click();
      await page.waitForURL('/');
      
      // Form should be cleared (or state should be handled appropriately)
      await expect(page.locator('textarea[name="concern"]')).toHaveValue('');
    });
  });

  test.describe('Accessibility', () => {
    test('should have proper ARIA labels', async ({ page }) => {
      // Check form accessibility
      await expect(page.locator('textarea[name="concern"]')).toHaveAttribute('aria-label');
      await expect(page.locator('textarea[name="context"]')).toHaveAttribute('aria-label');
      await expect(page.getByRole('button', { name: /check compliance/i })).toHaveAttribute('aria-label');
    });

    test('should support keyboard navigation', async ({ page }) => {
      // Navigate through form with keyboard
      await page.keyboard.press('Tab');
      await expect(page.locator('textarea[name="concern"]')).toBeFocused();
      
      await page.keyboard.press('Tab');
      await expect(page.locator('textarea[name="context"]')).toBeFocused();
      
      await page.keyboard.press('Tab');
      await expect(page.getByRole('button', { name: /check compliance/i })).toBeFocused();
    });

    test('should have proper heading structure', async ({ page }) => {
      // Check heading hierarchy
      const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
      expect(headings.length).toBeGreaterThan(0);
      
      // Check that main heading is h1
      await expect(page.locator('h1')).toBeVisible();
    });
  });

  test.describe('Mobile Responsiveness', () => {
    test('should work on mobile devices', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });
      
      // Check that form is usable on mobile
      await expect(page.locator('textarea[name="concern"]')).toBeVisible();
      await expect(page.locator('textarea[name="context"]')).toBeVisible();
      await expect(page.getByRole('button', { name: /check compliance/i })).toBeVisible();
      
      // Test form interaction on mobile
      await page.locator('textarea[name="concern"]').fill('Mobile test concern');
      await page.locator('textarea[name="context"]').fill('Mobile test context');
      
      await expect(page.locator('textarea[name="concern"]')).toHaveValue('Mobile test concern');
      await expect(page.locator('textarea[name="context"]')).toHaveValue('Mobile test context');
    });

    test('should have touch-friendly interface', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });
      
      // Check that buttons are large enough for touch
      const button = page.getByRole('button', { name: /check compliance/i });
      const buttonBox = await button.boundingBox();
      
      // Buttons should be at least 44px in height for touch accessibility
      expect(buttonBox.height).toBeGreaterThanOrEqual(44);
    });
  });
}); 
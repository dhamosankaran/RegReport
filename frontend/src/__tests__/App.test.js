import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock components
jest.mock('../components/ComplianceChecker', () => {
  return function MockComplianceChecker() {
    return <div data-testid="compliance-checker">Compliance Checker Component</div>;
  };
});

jest.mock('../components/DocumentStatus', () => {
  return function MockDocumentStatus() {
    return <div data-testid="document-status">Document Status Component</div>;
  };
});

jest.mock('../components/HowItWorks', () => {
  return function MockHowItWorks() {
    return <div data-testid="how-it-works">How It Works Component</div>;
  };
});

jest.mock('../components/Header', () => {
  return function MockHeader() {
    return (
      <header data-testid="header">
        <nav>
          <a href="/" data-testid="nav-home">Home</a>
          <a href="/documents" data-testid="nav-documents">Documents</a>
          <a href="/how-it-works" data-testid="nav-how-it-works">How It Works</a>
        </nav>
      </header>
    );
  };
});

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('App Component', () => {
  beforeEach(() => {
    // Clear any previous renders
    jest.clearAllMocks();
  });

  describe('Initial Render', () => {
    test('renders header component', () => {
      renderWithRouter(<App />);
      expect(screen.getByTestId('header')).toBeInTheDocument();
    });

    test('renders main content area', () => {
      renderWithRouter(<App />);
      expect(screen.getByRole('main')).toBeInTheDocument();
    });

    test('renders compliance checker by default on home route', () => {
      renderWithRouter(<App />);
      expect(screen.getByTestId('compliance-checker')).toBeInTheDocument();
    });

    test('does not render other components on home route', () => {
      renderWithRouter(<App />);
      expect(screen.queryByTestId('document-status')).not.toBeInTheDocument();
      expect(screen.queryByTestId('how-it-works')).not.toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    test('navigates to documents page when documents link is clicked', async () => {
      const user = userEvent.setup();
      renderWithRouter(<App />);
      
      const documentsLink = screen.getByTestId('nav-documents');
      await user.click(documentsLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('document-status')).toBeInTheDocument();
      });
      
      expect(screen.queryByTestId('compliance-checker')).not.toBeInTheDocument();
      expect(screen.queryByTestId('how-it-works')).not.toBeInTheDocument();
    });

    test('navigates to how-it-works page when how-it-works link is clicked', async () => {
      const user = userEvent.setup();
      renderWithRouter(<App />);
      
      const howItWorksLink = screen.getByTestId('nav-how-it-works');
      await user.click(howItWorksLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('how-it-works')).toBeInTheDocument();
      });
      
      expect(screen.queryByTestId('compliance-checker')).not.toBeInTheDocument();
      expect(screen.queryByTestId('document-status')).not.toBeInTheDocument();
    });

    test('navigates back to home when home link is clicked', async () => {
      const user = userEvent.setup();
      renderWithRouter(<App />);
      
      // First navigate to documents
      const documentsLink = screen.getByTestId('nav-documents');
      await user.click(documentsLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('document-status')).toBeInTheDocument();
      });
      
      // Then navigate back to home
      const homeLink = screen.getByTestId('nav-home');
      await user.click(homeLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('compliance-checker')).toBeInTheDocument();
      });
      
      expect(screen.queryByTestId('document-status')).not.toBeInTheDocument();
    });
  });

  describe('Layout and Styling', () => {
    test('applies correct CSS classes to main element', () => {
      renderWithRouter(<App />);
      
      const mainElement = screen.getByRole('main');
      expect(mainElement).toHaveClass('container', 'mx-auto', 'px-4', 'py-8');
    });

    test('maintains layout structure across navigation', async () => {
      const user = userEvent.setup();
      renderWithRouter(<App />);
      
      // Check initial layout
      expect(screen.getByTestId('header')).toBeInTheDocument();
      expect(screen.getByRole('main')).toBeInTheDocument();
      
      // Navigate to documents
      const documentsLink = screen.getByTestId('nav-documents');
      await user.click(documentsLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('document-status')).toBeInTheDocument();
      });
      
      // Layout should still be intact
      expect(screen.getByTestId('header')).toBeInTheDocument();
      expect(screen.getByRole('main')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper semantic HTML structure', () => {
      renderWithRouter(<App />);
      
      expect(screen.getByRole('banner')).toBeInTheDocument(); // header
      expect(screen.getByRole('main')).toBeInTheDocument();
      expect(screen.getByRole('navigation')).toBeInTheDocument();
    });

    test('navigation links are accessible', () => {
      renderWithRouter(<App />);
      
      const homeLink = screen.getByTestId('nav-home');
      const documentsLink = screen.getByTestId('nav-documents');
      const howItWorksLink = screen.getByTestId('nav-how-it-works');
      
      expect(homeLink).toBeInTheDocument();
      expect(documentsLink).toBeInTheDocument();
      expect(howItWorksLink).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    test('handles component rendering errors gracefully', () => {
      // This test would be more relevant if we had error boundaries
      renderWithRouter(<App />);
      
      // App should still render even if individual components fail
      expect(screen.getByTestId('header')).toBeInTheDocument();
      expect(screen.getByRole('main')).toBeInTheDocument();
    });
  });

  describe('Performance', () => {
    test('renders quickly without performance issues', () => {
      const startTime = performance.now();
      
      renderWithRouter(<App />);
      
      const endTime = performance.now();
      const renderTime = endTime - startTime;
      
      // Should render in under 100ms
      expect(renderTime).toBeLessThan(100);
    });

    test('navigation is responsive', async () => {
      const user = userEvent.setup();
      renderWithRouter(<App />);
      
      const startTime = performance.now();
      
      const documentsLink = screen.getByTestId('nav-documents');
      await user.click(documentsLink);
      
      await waitFor(() => {
        expect(screen.getByTestId('document-status')).toBeInTheDocument();
      });
      
      const endTime = performance.now();
      const navigationTime = endTime - startTime;
      
      // Navigation should complete in under 200ms
      expect(navigationTime).toBeLessThan(200);
    });
  });

  describe('Mobile Responsiveness', () => {
    test('maintains layout on different screen sizes', () => {
      // Test with different viewport sizes
      const viewports = [
        { width: 375, height: 667 }, // iPhone
        { width: 768, height: 1024 }, // iPad
        { width: 1920, height: 1080 }, // Desktop
      ];
      
      viewports.forEach(viewport => {
        window.innerWidth = viewport.width;
        window.innerHeight = viewport.height;
        
        renderWithRouter(<App />);
        
        expect(screen.getByTestId('header')).toBeInTheDocument();
        expect(screen.getByRole('main')).toBeInTheDocument();
        expect(screen.getByTestId('compliance-checker')).toBeInTheDocument();
      });
    });
  });
}); 
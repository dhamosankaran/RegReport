const { execSync } = require('child_process');
const { spawn } = require('child_process');

async function globalSetup() {
  console.log('Starting global setup for E2E tests...');
  
  // Start backend server if not already running
  try {
    console.log('Starting backend server...');
    const backendProcess = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'], {
      cwd: '../backend',
      stdio: 'pipe',
      detached: true
    });
    
    // Wait for backend to be ready
    await new Promise((resolve) => {
      const checkBackend = setInterval(async () => {
        try {
          const response = await fetch('http://localhost:8000/health');
          if (response.ok) {
            clearInterval(checkBackend);
            console.log('Backend server is ready');
            resolve();
          }
        } catch (error) {
          // Backend not ready yet, continue waiting
        }
      }, 1000);
      
      // Timeout after 30 seconds
      setTimeout(() => {
        clearInterval(checkBackend);
        console.log('Backend server startup timeout');
        resolve();
      }, 30000);
    });
    
    // Store process for cleanup
    global.backendProcess = backendProcess;
    
  } catch (error) {
    console.error('Failed to start backend server:', error);
  }
  
  // Start PostgreSQL if using Docker
  try {
    console.log('Starting PostgreSQL database...');
    execSync('docker-compose up -d postgres', { 
      cwd: '..',
      stdio: 'inherit' 
    });
    
    // Wait for PostgreSQL to be ready
    await new Promise((resolve) => {
      const checkPostgres = setInterval(() => {
        try {
          execSync('docker-compose exec -T postgres pg_isready -U postgres', { 
            cwd: '..',
            stdio: 'pipe' 
          });
          clearInterval(checkPostgres);
          console.log('PostgreSQL is ready');
          resolve();
        } catch (error) {
          // PostgreSQL not ready yet, continue waiting
        }
      }, 2000);
      
      // Timeout after 60 seconds
      setTimeout(() => {
        clearInterval(checkPostgres);
        console.log('PostgreSQL startup timeout');
        resolve();
      }, 60000);
    });
    
  } catch (error) {
    console.error('Failed to start PostgreSQL:', error);
  }
  
  console.log('Global setup completed');
}

module.exports = globalSetup; 
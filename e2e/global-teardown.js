const { execSync } = require('child_process');

async function globalTeardown() {
  console.log('Starting global teardown for E2E tests...');
  
  // Stop backend server
  if (global.backendProcess) {
    try {
      console.log('Stopping backend server...');
      global.backendProcess.kill('SIGTERM');
      await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for graceful shutdown
      
      if (!global.backendProcess.killed) {
        global.backendProcess.kill('SIGKILL');
      }
    } catch (error) {
      console.error('Error stopping backend server:', error);
    }
  }
  
  // Stop PostgreSQL
  try {
    console.log('Stopping PostgreSQL database...');
    execSync('docker-compose down', { 
      cwd: '..',
      stdio: 'inherit' 
    });
  } catch (error) {
    console.error('Error stopping PostgreSQL:', error);
  }
  
  // Clean up test data
  try {
    console.log('Cleaning up test data...');
    // No ChromaDB cleanup needed
  } catch (error) {
    console.error('Error cleaning up test data:', error);
  }
  
  console.log('Global teardown completed');
}

module.exports = globalTeardown; 
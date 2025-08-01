import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import SignUp from './SignUp';
import './App.css';

function MainApp() {
  const [inputCode, setInputCode] = useState(`// Example: Paste your C#, Java, Python, or JavaScript code here.
    public class Calculator
    {
        public int Add(int a, int b)
        {
            return a + b;
        }
    }`);

  const [generatedTests, setGeneratedTests] = useState(`// Example: Unit test for Calculator.Add
    [Test]
    public void Add_TwoNumbers_ReturnsCorrectSum()
    {
        Calculator calc = new Calculator();
        int result = calc.Add(5, 3);
        Assert.AreEqual(8, result);
    }

    // Example: Integration test for Calculator service
    [Test]
    public void CalculateService_AddsAndReturnsTotal()
    {
        // Arrange
        var service = new CalculatorService();
        // Act
        int total = service.CalculateTotal(10, 20);
        // Assert
        Assert.AreEqual(30, total);
    }`);

  const navigate = useNavigate();

  const handleGenerateTests = () => {
    // This would typically call your API
    console.log('Generating tests for:', inputCode);
  };

  const handleValidateConfig = () => {
    // This would typically validate configuration
    console.log('Validating configuration');
  };

  const handleSignUpClick = () => {
    navigate('/signup');
  };

  return (
    <div className="App">
      {/* Background Pattern */}
      <div className="background-pattern"></div>
      
      {/* Header Bar */}
      <nav className="header-bar">
        <div className="header-content">
          <div className="logo">
            <h2>Testmate.io</h2>
          </div>
          <div className="auth-buttons">
            <button className="btn btn-login">Login</button>
            <div className="signup-container">
              <button className="btn btn-signup" onClick={handleSignUpClick}>Sign In</button>
              <div className="tooltip">Create an account to maintain history</div>
            </div>
          </div>
        </div>
      </nav>
      
      {/* Header Section */}
      <header className="header">
        <h1 className="title"> Elevate Your Code Quality</h1>
        <p className="subtitle">
          Unlock the power of AI to generate comprehensive unit and integration tests.
          <br />
          Generate tests, Test, Validate and Optimize your code in one place.
        </p>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Paste Your Code Section */}
        <section className="code-section">
          <h2 className="section-title">Paste Your Code</h2>
          <p className="section-description">
            Input your code here for analysis. Our AI will process it to understand its structure and logic.
          </p>
          <div className="code-editor-container">
            <textarea
              className="code-editor"
              value={inputCode}
              onChange={(e) => setInputCode(e.target.value)}
              placeholder="Paste your code here..."
            />
          </div>
          <div className="button-group">
            <button className="btn btn-primary" onClick={handleGenerateTests}>
              Generate Tests
            </button>
            <button className="btn btn-secondary" onClick={handleValidateConfig}>
              Validate Config
            </button>
          </div>
        </section>

        {/* Generated Tests Section */}
        <section className="code-section">
          <h2 className="section-title">Generated Tests</h2>
          <p className="section-description">
            View the AI-generated unit and integration tests. Easily copy them into your project.
          </p>
          <div className="code-editor-container">
            <textarea
              className="code-editor"
              value={generatedTests}
              readOnly
              placeholder="Generated tests will appear here..."
            />
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p className="footer-text">
          Testmate.io leverages genAI models to analyse your code and automatically 
          generate relevant, high-quality unit and integration tests. Whether you're working with C#, 
          Java, Python, or JavaScript, our tool seamlessly integrates into your development workflow, 
          helping you maintain code integrity and accelerate your testing process.
        </p>
        <p className="footer-text">
          Github - <a href="https://github.com/abrarz2511/testmate.io" target="_blank" rel="noopener noreferrer">Testmate.io</a>
        </p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainApp />} />
        <Route path="/signup" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;

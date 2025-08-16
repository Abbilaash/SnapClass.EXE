import React from 'react';
import { Mail, Github, Heart, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="md:col-span-2">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-purple-500 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-sm">S</span>
              </div>
              <span className="text-xl font-bold">SnapClass</span>
            </div>
            <p className="text-gray-400 mb-6 max-w-md">
              An offline AI-powered classroom assistant that makes learning accessible everywhere. 
              Built with ❤️ for students and teachers worldwide.
            </p>
            
            {/* Hackathon Credit */}
            <div className="bg-gray-800 rounded-lg p-4 mb-6">
              <div className="flex items-center mb-2">
                <span className="text-purple-400 mr-2">🏆</span>
                <span className="font-semibold text-sm">Qualcomm Edge AI Hackathon</span>
              </div>
              <p className="text-gray-400 text-sm">
                Developed during the Qualcomm Edge AI Hackathon 2024, showcasing the power of on-device AI for education.
              </p>
            </div>

            <div className="flex space-x-4">
              <a 
                href="mailto:team@snapclass.ai" 
                className="bg-gray-800 hover:bg-gray-700 p-3 rounded-lg transition-colors duration-200 flex items-center"
              >
                <Mail size={20} className="mr-2" />
                <span className="text-sm">Contact Us</span>
              </a>
              <a 
                href="https://github.com/snapclass" 
                className="bg-gray-800 hover:bg-gray-700 p-3 rounded-lg transition-colors duration-200 flex items-center"
              >
                <Github size={20} className="mr-2" />
                <span className="text-sm">GitHub</span>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li><a href="#features" className="text-gray-400 hover:text-white transition-colors duration-200">Features</a></li>
              <li><a href="#how-it-works" className="text-gray-400 hover:text-white transition-colors duration-200">How It Works</a></li>
              <li><a href="#audience" className="text-gray-400 hover:text-white transition-colors duration-200">Who Uses It</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-200 flex items-center">
                Download App <ExternalLink size={14} className="ml-1" />
              </a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li><a href="#team" className="text-gray-400 hover:text-white transition-colors duration-200">Our Team</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">Terms of Service</a></li>
              <li><a href="mailto:support@snapclass.ai" className="text-gray-400 hover:text-white transition-colors duration-200">Support</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © 2024 SnapClass. All rights reserved. Built with{' '}
              <Heart size={14} className="inline text-red-500" />{' '}
              for education.
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center text-sm text-gray-400">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                <span>Status: Active Development</span>
              </div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-gray-800">
            <p className="text-center text-xs text-gray-500">
              This project demonstrates edge AI capabilities for educational applications. 
              All AI processing occurs on-device to ensure privacy and offline functionality.
              <br />
              <span className="text-purple-400">Powered by Qualcomm Edge AI Technology</span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
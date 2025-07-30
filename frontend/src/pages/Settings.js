import React from 'react';
import { useAuth } from '../contexts/AuthContext';

function Settings() {
  const { user } = useAuth();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">设置</h1>
        <p className="mt-2 text-sm text-gray-600">
          管理您的账户设置和系统配置。
        </p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            账户信息
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                用户名
              </label>
              <p className="mt-1 text-sm text-gray-900">{user?.username}</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">
                邮箱
              </label>
              <p className="mt-1 text-sm text-gray-900">{user?.email}</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">
                角色
              </label>
              <p className="mt-1 text-sm text-gray-900">{user?.role}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            系统信息
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                版本
              </label>
              <p className="mt-1 text-sm text-gray-900">1.0.0</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">
                状态
              </label>
              <p className="mt-1 text-sm text-green-600">运行正常</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
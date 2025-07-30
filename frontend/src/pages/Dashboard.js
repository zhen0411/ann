import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { fetchProjects } from '../store/slices/projectsSlice';
import {
  FolderIcon,
  VideoCameraIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

function Dashboard() {
  const dispatch = useDispatch();
  const { projects, loading } = useSelector((state) => state.projects);
  const { user } = useSelector((state) => state.auth);

  useEffect(() => {
    dispatch(fetchProjects());
  }, [dispatch]);

  const stats = [
    { name: '总项目数', value: projects.length, icon: FolderIcon },
    { name: '活跃项目', value: projects.filter(p => p.is_active).length, icon: CheckCircleIcon },
    { name: '待处理', value: 0, icon: ClockIcon },
    { name: '已完成', value: 0, icon: CheckCircleIcon },
  ];

  const recentProjects = projects.slice(0, 5);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">仪表板</h1>
        <p className="mt-2 text-sm text-gray-600">
          欢迎回来，{user?.username}！这里是您的标注工作概览。
        </p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((item) => (
          <div
            key={item.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <item.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {item.name}
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {item.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* 最近项目 */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            最近项目
          </h3>
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            </div>
          ) : recentProjects.length > 0 ? (
            <div className="space-y-4">
              {recentProjects.map((project) => (
                <div
                  key={project.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  <div className="flex items-center">
                    <FolderIcon className="h-8 w-8 text-blue-500 mr-3" />
                    <div>
                      <h4 className="text-sm font-medium text-gray-900">
                        {project.name}
                      </h4>
                      <p className="text-sm text-gray-500">
                        {project.description || '暂无描述'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        project.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {project.is_active ? '活跃' : '非活跃'}
                    </span>
                    <Link
                      to={`/projects/${project.id}`}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      查看详情
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FolderIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">暂无项目</h3>
              <p className="mt-1 text-sm text-gray-500">
                开始创建您的第一个标注项目。
              </p>
              <div className="mt-6">
                <Link
                  to="/projects"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                >
                  创建项目
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 快速操作 */}
      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <VideoCameraIcon className="h-6 w-6 text-blue-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    上传媒体文件
                  </dt>
                  <dd className="text-sm text-gray-900">
                    上传视频或音频文件进行标注
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <Link
                to="/media"
                className="text-sm font-medium text-blue-600 hover:text-blue-500"
              >
                开始上传 →
              </Link>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-6 w-6 text-green-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    审阅标注
                  </dt>
                  <dd className="text-sm text-gray-900">
                    审阅和批准标注结果
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <Link
                to="/projects"
                className="text-sm font-medium text-green-600 hover:text-green-500"
              >
                查看项目 →
              </Link>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-6 w-6 text-yellow-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    系统状态
                  </dt>
                  <dd className="text-sm text-gray-900">
                    查看系统运行状态和性能
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-4">
              <Link
                to="/settings"
                className="text-sm font-medium text-yellow-600 hover:text-yellow-500"
              >
                系统设置 →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
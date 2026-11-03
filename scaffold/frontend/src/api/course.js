import request from '@/utils/request'

/**
 * 课程列表（可按名称/编码/简介模糊查询）
 */
export function listCoursesApi(params) {
  return request({
    url: '/api/courses',
    method: 'get',
    params
  })
}

/**
 * 新增课程
 */
export function createCourseApi(data) {
  return request({
    url: '/api/courses',
    method: 'post',
    data
  })
}

/**
 * 修改课程
 */
export function updateCourseApi(courseId, data) {
  return request({
    url: `/api/courses/${courseId}`,
    method: 'put',
    data
  })
}

/**
 * 删除课程
 */
export function deleteCourseApi(courseId) {
  return request({
    url: `/api/courses/${courseId}`,
    method: 'delete'
  })
}

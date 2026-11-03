import request from '@/utils/request'

/**
 * 课表分页列表
 * 学生：不传 user_id，后端按 JWT 只返回本人课表
 * 管理员：可传 user_id 筛选某个学生，不传则看全部
 */
export function listSchedulesApi(params) {
  return request({
    url: '/api/schedules',
    method: 'get',
    params
  })
}

/**
 * 管理员新增课表
 */
export function createScheduleApi(data) {
  return request({
    url: '/api/schedules',
    method: 'post',
    data
  })
}

/**
 * 管理员修改课表
 */
export function updateScheduleApi(scheduleId, data) {
  return request({
    url: `/api/schedules/${scheduleId}`,
    method: 'put',
    data
  })
}

/**
 * 管理员删除课表
 */
export function deleteScheduleApi(scheduleId) {
  return request({
    url: `/api/schedules/${scheduleId}`,
    method: 'delete'
  })
}

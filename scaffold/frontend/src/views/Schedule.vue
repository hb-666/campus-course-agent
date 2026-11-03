<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>我的课表</span>
          <span v-if="isAdmin" style="font-size: 13px; font-weight: normal; color: #909399">
            （管理员视图：可查看全部学生并维护课表）
          </span>
        </div>
      </template>

      <div style="margin-bottom: 10px">
        <el-date-picker
          v-model="params.date"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="按上课日期筛选"
          style="width: 180px; margin-right: 8px"
          :clearable="true"
          @change="handleSearch"
        />
        <el-select
          v-if="isAdmin"
          v-model="params.userId"
          placeholder="选择学生"
          style="width: 160px; margin-right: 8px"
          clearable
          @change="handleSearch"
        >
          <el-option
            v-for="s in students"
            :key="s.id"
            :label="`${s.name}（${s.username}）`"
            :value="s.id"
          />
        </el-select>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button v-if="isAdmin" type="success" :icon="Plus" @click="handleCreate">新增</el-button>
      </div>

      <el-table
        :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333' }"
        :data="tableData"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column v-if="isAdmin" prop="user_name" label="学生" width="110">
          <template #default="{ row }">
            {{ row.user_name }}<span style="color: #909399">（{{ row.username }}）</span>
          </template>
        </el-table-column>
        <el-table-column prop="class_date" label="上课日期" width="130" />
        <el-table-column prop="period" label="节次" width="120" />
        <el-table-column prop="course_name" label="课程" min-width="150" />
        <el-table-column prop="location" label="地点" min-width="150">
          <template #default="{ row }">
            <span>{{ row.location || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column v-if="isAdmin" label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" text bg @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" text bg @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 10px; display: flex; justify-content: flex-end">
        <el-pagination
          v-model:current-page="params.page"
          v-model:page-size="params.pageSize"
          :total="total"
          background
          layout="total, prev, pager, next"
          @current-change="load"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑课表' : '新增课表'" width="500">
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        label-width="90px"
        style="width: 100%; padding-right: 30px; padding-top: 16px"
        v-loading="formLoading"
      >
        <el-form-item label="学生" prop="user_id">
          <el-select v-model="form.user_id" placeholder="请选择学生" style="width: 100%">
            <el-option
              v-for="s in students"
              :key="s.id"
              :label="`${s.name}（${s.username}）`"
              :value="s.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="课程" prop="course_id">
          <el-select v-model="form.course_id" placeholder="请选择课程" style="width: 100%">
            <el-option
              v-for="c in courses"
              :key="c.id"
              :label="`${c.name}（${c.code}）`"
              :value="c.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="上课日期" prop="class_date">
          <el-date-picker
            v-model="form.class_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="请选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="节次" prop="period">
          <el-input v-model="form.period" placeholder="如 第1-2节" />
        </el-form-item>
        <el-form-item label="地点" prop="location">
          <el-input v-model="form.location" placeholder="如 计算机楼 A301" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saveLoading" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'Schedule' })
import { Search, Plus } from '@element-plus/icons-vue'
import {
  createScheduleApi,
  deleteScheduleApi,
  listSchedulesApi,
  updateScheduleApi
} from '@/api/schedule'
import { listCoursesApi } from '@/api/course'
import { getUserPageList } from '@/api/user'
import { useUser } from '@/utils/user'
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const { userInfo } = useUser()
const isAdmin = computed(() => userInfo.value?.role === 'admin')

const params = reactive({
  page: 1,
  pageSize: 10,
  date: null,
  userId: null
})

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const formRef = ref()
const formLoading = ref(false)
const saveLoading = ref(false)

const students = ref([])
const courses = ref([])

const form = reactive({
  id: null,
  user_id: null,
  course_id: null,
  class_date: '',
  period: '',
  location: ''
})

const rules = {
  user_id: [{ required: true, message: '请选择学生', trigger: 'change' }],
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  class_date: [{ required: true, message: '请选择上课日期', trigger: 'change' }],
  period: [{ required: true, message: '请输入节次', trigger: 'blur' }]
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    user_id: null,
    course_id: null,
    class_date: '',
    period: '',
    location: ''
  })
}

// 管理员下拉框用：拉学生列表（只取 student 角色）和课程列表
const loadOptions = async () => {
  if (!isAdmin.value) return
  try {
    const userRes = await getUserPageList({ page: 1, page_size: 100 })
    if (userRes.code === 200) {
      students.value = (userRes.data?.list || []).filter((u) => u.role === 'student')
    }
  } catch {
    /* 忽略：下拉选项拉取失败不阻塞列表 */
  }
  try {
    const courseRes = await listCoursesApi({})
    if (courseRes.code === 200) {
      courses.value = courseRes.data || []
    }
  } catch {
    /* 同上 */
  }
}

const handleCreate = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, {
    id: row.id,
    user_id: row.user_id,
    course_id: row.course_id,
    class_date: row.class_date,
    period: row.period,
    location: row.location || ''
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确认删除 ${row.user_name} 在 ${row.class_date} 的 ${row.course_name} ？`,
    '确认删除',
    { type: 'warning' }
  ).then(async () => {
    const res = await deleteScheduleApi(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      load()
    }
  })
}

const handleSave = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  saveLoading.value = true
  try {
    const payload = {
      user_id: form.user_id,
      course_id: form.course_id,
      class_date: form.class_date,
      period: form.period,
      location: form.location
    }
    let res
    if (form.id) {
      res = await updateScheduleApi(form.id, payload)
    } else {
      res = await createScheduleApi(payload)
    }
    if (res.code === 200) {
      dialogVisible.value = false
      ElMessage.success('操作成功')
      load()
    }
  } finally {
    saveLoading.value = false
  }
}

const load = async () => {
  loading.value = true
  try {
    const query = {
      page: params.page,
      page_size: params.pageSize
    }
    if (params.date) query.date = params.date
    // 学生不传 user_id（后端按 JWT 限制），管理员仅在选了学生时传
    if (isAdmin.value && params.userId) query.user_id = params.userId

    const res = await listSchedulesApi(query)
    if (res.code === 200) {
      tableData.value = res.data?.list || []
      total.value = res.data?.total || 0
    }
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  params.page = 1
  load()
}

onMounted(async () => {
  await loadOptions()
  load()
})
</script>

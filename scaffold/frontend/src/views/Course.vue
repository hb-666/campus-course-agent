<template>
  <div>
    <el-card>
      <template #header>
        <div style="font-size: 16px; font-weight: bold">
          <span>课程管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px">
        <el-input
          v-model="keywords"
          placeholder="按名称 / 代码 / 简介查询"
          style="width: 240px; margin-right: 8px"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleSearch"
        ></el-input>
        <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
        <el-button type="success" :icon="Plus" @click="handleCreate">新增</el-button>
      </div>

      <el-table
        :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#333' }"
        :data="tableData"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="name" label="课程名称" min-width="140" />
        <el-table-column prop="code" label="课程代码" width="140" />
        <el-table-column prop="description" label="课程简介" min-width="240">
          <template #default="{ row }">
            <span>{{ row.description || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '正常' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" text bg @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" text bg @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑课程' : '新增课程'" width="480">
      <el-form
        ref="formRef"
        :rules="rules"
        :model="form"
        label-width="90px"
        style="width: 100%; padding-right: 30px; padding-top: 16px"
        v-loading="formLoading"
      >
        <el-form-item label="课程名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程代码" prop="code">
          <el-input v-model="form.code" placeholder="如 DS101，需唯一" />
        </el-form-item>
        <el-form-item label="课程简介" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="可选"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :value="1">正常</el-radio>
            <el-radio :value="0">停用</el-radio>
          </el-radio-group>
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
defineOptions({ name: 'Course' })
import { Search, Plus } from '@element-plus/icons-vue'
import { createCourseApi, deleteCourseApi, listCoursesApi, updateCourseApi } from '@/api/course'
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const keywords = ref('')
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formRef = ref()
const formLoading = ref(false)
const saveLoading = ref(false)

const form = reactive({
  id: null,
  name: '',
  code: '',
  description: '',
  status: 1
})

const rules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入课程代码', trigger: 'blur' }]
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    name: '',
    code: '',
    description: '',
    status: 1
  })
}

const handleCreate = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, {
    id: row.id,
    name: row.name,
    code: row.code,
    description: row.description || '',
    status: row.status
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除课程 [${row.name}] ？`, '确认删除', {
    type: 'warning'
  }).then(async () => {
    const res = await deleteCourseApi(row.id)
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
      name: form.name,
      code: form.code,
      description: form.description || null,
      status: form.status
    }
    let res
    if (form.id) {
      res = await updateCourseApi(form.id, payload)
    } else {
      res = await createCourseApi(payload)
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
    const res = await listCoursesApi({ keywords: keywords.value || undefined })
    if (res.code === 200) {
      tableData.value = res.data || []
    }
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  load()
}

onMounted(() => {
  load()
})
</script>

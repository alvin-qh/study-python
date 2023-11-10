# 员工查询片段
FRAGMENT_EMPLOYEE = """
    fragment employeeFields on Employee {
        id
        name
        gender
        role {
            name
        }
    }
"""

# 员工明细查询片段
FRAGMENT_EMPLOYEE_DETAIL = """
    fragment employeeDetailFields on Employee {
        ...employeeFields  # 员工信息, 引用员工查询片段
        department {       # 员工所属部门
            id
            name
            level
            manager {
                ...employeeFields  # 部门主管, 引用员工查询片段
            }
        }
    }
"""

# 根据部门名称查询部门信息
QUERY_DEPARTMENT_BY_NAME = (
    FRAGMENT_EMPLOYEE  # 包含员工查询片段
    + """
    query($name: String!) {
        department(name: $name) {  # 定义 name 参数, 查询部门信息
            id
            name
            level
            manager { # 部门主管, 包含员工查询片段
                ...employeeFields
            }
        }
    }
"""
)

# 根据员工姓名查询员工信息
QUERY_EMPLOYEE_BY_NAME = (
    FRAGMENT_EMPLOYEE  # 包含员工查询片段
    + FRAGMENT_EMPLOYEE_DETAIL  # 包含员工明细查询片段
    + """
        query($name: String!) {
            employee(name: $name) {  # 定义 name 参数, 查询员工信息
                ...employeeDetailFields  # 包含员工明细信息
            }
        }
      """
)

# 根据部门名称查询部门下所有员工列表
QUERY_EMPLOYEES_BY_DEPARTMENT = """
    query($departmentName: String!, $first: Int, $after: String) {
        employees(departmentName: $departmentName, first: $first, after: $after) {  # 定义查询参数
            edges {   # 查询列表, 分页查询
                node {
                    id
                    name
                    gender
                    role {
                        name
                    }
                    department {
                        id
                    }
                }
            }
            pageInfo {   # 分页信息
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""

# 创建一个部门
CREATE_DEPARTMENT = """
    mutation($createDepartmentInput: CreateDepartmentInput!) {
        createDepartment(input: $createDepartmentInput) {
            id
            name
        }
    }
"""

# 创建一个员工
CREATE_EMPLOYEE = """
    mutation($createEmployeeInput: CreateEmployeeInput!) {
        createEmployee(input: $createEmployeeInput) {
            id
            name
        }
    }
"""

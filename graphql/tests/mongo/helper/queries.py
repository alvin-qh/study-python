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

FRAGMENT_EMPLOYEE_DETAIL = """
    fragment employeeDetailFields on Employee {
        id
        name
        gender
        role {
            name
        }
        department {
            id
            name
            level
            manager {
                ...employeeFields
            }
        }
    }
"""

QUERY_DEPARTMENT_BY_NAME = (
    FRAGMENT_EMPLOYEE
    + """
    query($name: String!) {
        department(name: $name) {
            id
            name
            level
            manager {
                ...employeeFields
            }
        }
    }
"""
)

QUERY_EMPLOYEE_BY_NAME = (
    FRAGMENT_EMPLOYEE
    + FRAGMENT_EMPLOYEE_DETAIL
    + """
    query($name: String!) {
        employee(name: $name) {
            ...employeeDetailFields
        }
    }
"""
)

QUERY_EMPLOYEES_BY_DEPARTMENT = """
    query($departmentName: String!, $first: Int, $after: String) {
        employees(departmentName: $departmentName, first: $first, after: $after) {
            edges {
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
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
        }
    }
"""

CREATE_DEPARTMENT = """
    mutation($departmentInput: DepartmentInput!) {
        departmentMutation(input: {departmentInput: $departmentInput}) {
            department {
                id
                name
                level
            }
        }
    }
"""


CREATE_EMPLOYEE = """
    mutation($employeeInput: EmployeeInput!) {
        employeeMutation(input: {employeeInput: $employeeInput}) {
            employee {
                id
                name
                gender
                department {
                    id
                    name
                    level
                }
                role {
                    name
                }
            }
        }
    }
"""

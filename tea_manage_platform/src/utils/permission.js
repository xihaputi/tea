/*
* v-permission 指令
* 使用: v-permission="['admin', 'super_admin']"
*/
export default {
    mounted(el, binding) {
        const { value } = binding
        const roles = JSON.parse(localStorage.getItem('tea_roles') || '[]')

        // 如果是超级管理员，默认拥有所有权限
        // 假设 'super_admin' 是超级管理员角色，或者 admin 用户名为 admin
        // 简单起见，如果 roles 包含 super_admin 或 (admin 且 username=admin) 则认为是超管
        // 但前端判断 username 不太安全，主要依赖 roles

        // 逻辑：如果当前用户角色中 包含 指令要求的 ANY role，则显示
        // 同时，Super Admin 拥有所有权限 (除非指令特别排除? 通常不)

        const isSuperAdmin = roles.includes('super_admin') || (roles.includes('admin') && localStorage.getItem('tea_user') && JSON.parse(localStorage.getItem('tea_user')).name === '超级管理员')

        if (isSuperAdmin) {
            return
        }

        if (value && value instanceof Array && value.length > 0) {
            const permissionRoles = value
            const hasPermission = roles.some(role => {
                return permissionRoles.includes(role)
            })

            if (!hasPermission) {
                el.parentNode && el.parentNode.removeChild(el)
            }
        } else {
            throw new Error(`need roles! Like v-permission="['admin','editor']"`)
        }
    }
}

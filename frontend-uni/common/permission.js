export function hasPermission(requiredRoles) {
    const roles = uni.getStorageSync('roles') || [];
    const userInfo = uni.getStorageSync('userInfo') || {};

    // 超级管理员权限
    if (roles.includes('super_admin') || (roles.includes('admin') && userInfo.username === 'admin')) {
        return true;
    }

    if (!requiredRoles || requiredRoles.length === 0) {
        return true;
    }

    return roles.some(role => requiredRoles.includes(role));
}

export function isSuperAdmin() {
    const roles = uni.getStorageSync('roles') || [];
    const userInfo = uni.getStorageSync('userInfo') || {};
    return roles.includes('super_admin') || (roles.includes('admin') && userInfo.username === 'admin');
}

export function isAdmin() {
    const roles = uni.getStorageSync('roles') || [];
    return roles.includes('admin') || isSuperAdmin();
}

/** @odoo-module **/

import { registry } from "@web/core/registry";

/**
 * Login Notifications Service
 * Hooks into the existing WEB_CLIENT_READY event to show login notifications
 * This avoids asset bundle conflicts by using existing Odoo web architecture
 */
export const loginNotificationService = {
    dependencies: ["notification", "orm"],

    start(env, { notification, orm }) {
        console.log('🔔 Login Notifications Service: Starting...');

        // Hook into the existing WEB_CLIENT_READY event
        const handleWebClientReady = async () => {
            console.log('🔔 Login Notifications Service: Web client ready, checking for notifications...');
            
            try {
                await checkLoginNotifications(orm, notification);
            } catch (error) {
                console.error('🔔 Login Notifications Service: Error during notification check:', error);
            }
        };

        // Listen to the existing WEB_CLIENT_READY event
        env.bus.addEventListener("WEB_CLIENT_READY", handleWebClientReady);

        return {
            checkLoginNotifications: () => checkLoginNotifications(orm, notification),
        };
    },
};

/**
 * Check for login notifications and display popup if needed
 */
async function checkLoginNotifications(orm, notification) {
    try {
        console.log('🔔 Login Notifications: Making RPC call to check notifications...');

        // Add a small delay to ensure Odoo is fully loaded
        setTimeout(async () => {
            try {
                // Call our backend method
                const result = await orm.call(
                    'res.users',
                    'check_login_notifications',
                    []
                );

                console.log('🔔 Login Notifications: RPC response:', result);

                if (result && result.show_popup) {
                    displayLoginNotificationPopup(result, notification);
                } else {
                    console.log('🔔 Login Notifications: No notifications to show');
                }
            } catch (error) {
                console.error('🔔 Login Notifications: RPC call failed:', error);
                // Optionally show a user-friendly error notification
                if (error.message && !error.message.includes('404')) {
                    notification.add('Failed to check login notifications. Please try refreshing the page.', {
                        title: "⚠️ Notification Error",
                        type: "warning",
                    });
                }
            }
        }, 1000); // 1 second delay to ensure everything is loaded
        
    } catch (error) {
        console.error('🔔 Login Notifications: Unexpected error:', error);
    }
}

/**
 * Display the notification popup with overdue and due items
 */
function displayLoginNotificationPopup(data, notification) {
    console.log('🔔 Login Notifications: Displaying popup with data:', data);

    let message = '<div class="login-notification-popup">';
    
    if (data.overdue_items && data.overdue_items.length > 0) {
        message += '<h4 style="color: #d9534f; margin: 15px 0 8px 0; font-weight: 600;">⚠️ Overdue Items (' + data.overdue_items.length + ')</h4>';
        message += '<ul style="margin: 8px 0 15px 20px; padding: 0; list-style-type: disc;">';
        data.overdue_items.forEach(item => {
            message += '<li style="margin: 5px 0; padding: 3px 0;"><strong>' + (item.name || 'Unknown') + '</strong>';
            if (item.days_overdue) {
                message += ' <span class="overdue-days" style="color: #d9534f; font-weight: 500;">(' + item.days_overdue + ' days overdue)</span>';
            }
            message += '</li>';
        });
        message += '</ul>';
    }
    
    if (data.due_today_items && data.due_today_items.length > 0) {
        message += '<h4 style="color: #f0ad4e; margin: 15px 0 8px 0; font-weight: 600;">📅 Due Today (' + data.due_today_items.length + ')</h4>';
        message += '<ul style="margin: 8px 0 15px 20px; padding: 0; list-style-type: disc;">';
        data.due_today_items.forEach(item => {
            message += '<li style="margin: 5px 0; padding: 3px 0;"><strong>' + (item.name || 'Unknown') + '</strong></li>';
        });
        message += '</ul>';
    }

    message += '<p class="footer-text" style="margin: 15px 0 5px 0; font-size: 12px; color: #6c757d; font-style: italic; border-top: 1px solid #e9ecef; padding-top: 10px;">This notification appears once per day.</p>';
    message += '</div>';

    // Use Odoo's notification service to show the popup
    notification.add(message, {
        title: "📋 Login Notifications",
        type: "info",
        sticky: true,  // Keep the notification visible until dismissed
    });
}

// Register the service
registry.category("services").add("login_notifications", loginNotificationService);

// Global access for testing (only in debug mode)
if (typeof odoo !== 'undefined' && odoo.debug) {
    window.testLoginNotifications = async () => {
        try {
            const services = odoo.__DEBUG__.services;
            const loginService = services['login_notifications'];
            if (loginService && loginService.checkLoginNotifications) {
                await loginService.checkLoginNotifications();
                console.log('✅ Test login notifications triggered');
            } else {
                console.error('❌ Login notification service not available');
                // Try to get services directly
                const orm = services['orm'];
                const notification = services['notification'];
                if (orm && notification) {
                    console.log('🔄 Trying direct service call...');
                    await checkLoginNotifications(orm, notification);
                } else {
                    console.error('❌ ORM or Notification services not available');
                }
            }
        } catch (error) {
            console.error('❌ Test failed:', error);
        }
    };
    
    window.testLoginNotificationsWithData = () => {
        try {
            const services = odoo.__DEBUG__.services;
            const notification = services['notification'];
            if (notification) {
                // Test with dummy data
                const testData = {
                    show_popup: true,
                    overdue_items: [
                        { name: 'ISO 9001:2015 Quality Management', type: 'Standard', days_overdue: 5 },
                        { name: 'Document Control Domain', type: 'Domain', days_overdue: 3 }
                    ],
                    due_today_items: [
                        { name: 'ISO 14001:2015 Environmental', type: 'Standard' },
                        { name: 'Risk Assessment Domain', type: 'Domain' }
                    ]
                };
                displayLoginNotificationPopup(testData, notification);
                console.log('✅ Test popup displayed with dummy data');
            } else {
                console.error('❌ Notification service not available');
            }
        } catch (error) {
            console.error('❌ Test with data failed:', error);
        }
    };
    
    window.resetLoginNotificationFlag = async () => {
        try {
            const services = odoo.__DEBUG__.services;
            const orm = services['orm'];
            if (orm) {
                const result = await orm.call('res.users', 'reset_login_notification', []);
                console.log('✅ Reset result:', result);
            } else {
                console.error('❌ ORM service not available');
            }
        } catch (error) {
            console.error('❌ Reset failed:', error);
        }
    };
}
from locust import User, tag, task, between
import mysql.connector
import random
import time,os

class DatabaseUser(User):
    wait_time = between(1, 3)  # 请求间隔 1~3 秒

    def on_start(self):
        """初始化数据库连接"""
        self.db = mysql.connector.connect(
            host="10.0.0.197",
            user="root",
            password="123456",
            database="awdtsg_prod"
        )
        self.cursor = self.db.cursor(buffered=True) 

    @task(2)
    def query_data(self):
        """执行随机查询"""
        query = """
            SELECT `PostComment`.`id`, `PostComment`.`message`, `PostComment`.`postId`, 
                   `PostComment`.`userId`, `PostComment`.`isAnonymous`, `PostComment`.`archived`, 
                   `PostComment`.`parentCommentId`, `PostComment`.`imageUrl`, `PostComment`.`likeCount`, 
                   `PostComment`.`level`, `PostComment`.`createdAt`, `PostComment`.`updatedAt`, 
                   (SELECT COUNT(*) FROM UserBlocks 
                    WHERE (PostComment.userId = UserBlocks.blockedUserId 
                           AND PostComment.isAnonymous = UserBlocks.isBlockedUserAnonymous 
                           AND UserBlocks.userId = %s) 
                       OR (PostComment.userId = UserBlocks.userId 
                           AND UserBlocks.blockedUserId = %s 
                           AND PostComment.isAnonymous = UserBlocks.isBlockedUserAnonymous)) 
                   AS `blockedUserCount`, 
                   `post`.`id` AS `post.id`, `post`.`message` AS `post.message`, 
                   `post`.`userId` AS `post.userId`, `post`.`groupId` AS `post.groupId`, 
                   `post`.`isAnonymous` AS `post.isAnonymous`, `post`.`archived` AS `post.archived`, 
                   `post`.`links` AS `post.links`, `post`.`typeId` AS `post.typeId`, 
                   `post`.`adminPostId` AS `post.adminPostId`, `post`.`createdAt` AS `post.createdAt`, 
                   `post`.`updatedAt` AS `post.updatedAt` 
            FROM `PostComments` AS `PostComment` 
            LEFT OUTER JOIN `Posts` AS `post` ON `PostComment`.`postId` = `post`.`id` 
            WHERE `PostComment`.`message` LIKE %s 
            HAVING `blockedUserCount` = 0 
            ORDER BY `PostComment`.`createdAt` DESC 
            LIMIT 0,100
        """
        params = (221606, 221606, '%mikc%')  # 使用占位符绑定参数
        start_time = time.time()
        try:
            self.cursor.execute(query, params)
            self.cursor.fetchall()  # 获取所有结果集
            self.db.commit()  # 确保事务提交
            self.environment.events.request.fire(
                request_type="SQL",
                name="query_data",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                success=True,  # 表示请求成功
            )
            
        except Exception as e:
            self.environment.events.request.fire(
                request_type="SQL",
                name="query_data",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                exception=e,
                success=False,  # 表示请求失败
            )
  
    @task(1)
    def query2_data(self):
        """执行随机查询"""
        query = """
            SELECT `User`.`id`, `User`.`firstName`, `User`.`lastName`, `User`.`email`, `User`.`role`, `User`.`lastLoggedIn`, `User`.`appIdentifier`, `User`.`profilePictureURL`, `User`.`socialId`, `User`.`acceptedTerms`, `User`.`socialAuthType`, `User`.`isBanned`, `User`.`isSuspended`, `User`.`suspendedUntil`, `User`.`coordinates`, `User`.`reasonRejected`, `User`.`profilePictureKey`, `User`.`facebookGroupIds`, `User`.`facebookUserId`, `User`.`awdtsgFacebookUserId`, `User`.`activeGroup`, `User`.`lastSeenNotification`, `User`.`rejectedGroupId`, `User`.`archived`, `User`.`createdAt`, `User`.`updatedAt`, (SELECT COUNT(*) FROM UserBlocks WHERE User.id = UserBlocks.blockedUserId && UserBlocks.isBlockedUserAnonymous = 0 && UserBlocks.userId = %s) AS `blockedUserCount`, `groups`.`id` AS `groups.id`, `groups`.`city` AS `groups.city`, `groups`.`state` AS `groups.state`, `groups`.`country` AS `groups.country`, `groups`.`zipCode` AS `groups.zipCode`, `groups`.`latitude` AS `groups.latitude`, `groups`.`longitude` AS `groups.longitude`, `groups`.`milesRange` AS `groups.milesRange`, `groups`.`facebookGroupId` AS `groups.facebookGroupId`, `groups`.`createdAt` AS `groups.createdAt`, `groups`.`updatedAt` AS `groups.updatedAt`, `groups->UserGroup`.`id` AS `groups.UserGroup.id`, `groups->UserGroup`.`userId` AS `groups.UserGroup.userId`, `groups->UserGroup`.`groupId` AS `groups.UserGroup.groupId`, `groups->UserGroup`.`createdAt` AS `groups.UserGroup.createdAt`, `groups->UserGroup`.`updatedAt` AS `groups.UserGroup.updatedAt`, `permissions`.`id` AS `permissions.id`, `permissions`.`name` AS `permissions.name`, `permissions`.`description` AS `permissions.description`, `permissions`.`owner` AS `permissions.owner`, `permissions`.`admin` AS `permissions.admin`, `permissions`.`moderator` AS `permissions.moderator`, `permissions`.`user` AS `permissions.user`, `permissions`.`createdAt` AS `permissions.createdAt`, `permissions`.`updatedAt` AS `permissions.updatedAt`, `permissions->UserPermission`.`id` AS `permissions.UserPermission.id`, `permissions->UserPermission`.`userId` AS `permissions.UserPermission.userId`, `permissions->UserPermission`.`permissionId` AS `permissions.UserPermission.permissionId`, `permissions->UserPermission`.`enabled` AS `permissions.UserPermission.enabled`, `groupRequest`.`id` AS `groupRequest.id`, `groupRequest`.`groupName` AS `groupRequest.groupName`, `groupRequest`.`userFirstName` AS `groupRequest.userFirstName`, `groupRequest`.`userLastName` AS `groupRequest.userLastName`, `groupRequest`.`userPictureKey` AS `groupRequest.userPictureKey`, `groupRequest`.`groupUrl` AS `groupRequest.groupUrl`, `groupRequest`.`accepted` AS `groupRequest.accepted`, `groupRequest`.`acceptedById` AS `groupRequest.acceptedById`, `groupRequest`.`acceptedAt` AS `groupRequest.acceptedAt`, `groupRequest`.`userId` AS `groupRequest.userId`, `groupRequest`.`groupId` AS `groupRequest.groupId`, `groupRequest`.`createdAt` AS `groupRequest.createdAt`, `groupRequest`.`updatedAt` AS `groupRequest.updatedAt`, `rejectedGroup`.`id` AS `rejectedGroup.id`, `rejectedGroup`.`city` AS `rejectedGroup.city`, `rejectedGroup`.`state` AS `rejectedGroup.state`, `rejectedGroup`.`country` AS `rejectedGroup.country`, `rejectedGroup`.`zipCode` AS `rejectedGroup.zipCode`, `rejectedGroup`.`latitude` AS `rejectedGroup.latitude`, `rejectedGroup`.`longitude` AS `rejectedGroup.longitude`, `rejectedGroup`.`milesRange` AS `rejectedGroup.milesRange`, `rejectedGroup`.`facebookGroupId` AS `rejectedGroup.facebookGroupId`, `rejectedGroup`.`createdAt` AS `rejectedGroup.createdAt`, `rejectedGroup`.`updatedAt` AS `rejectedGroup.updatedAt`, `UserGroup`.`id` AS `UserGroup.id`, `UserGroup`.`userId` AS `UserGroup.userId`, `UserGroup`.`groupId` AS `UserGroup.groupId`, `UserGroup`.`createdAt` AS `UserGroup.createdAt`, `UserGroup`.`updatedAt` AS `UserGroup.updatedAt`, `UserGroup->user`.`id` AS `UserGroup.user.id`, `UserGroup->user`.`firstName` AS `UserGroup.user.firstName`, `UserGroup->user`.`lastName` AS `UserGroup.user.lastName`, `UserGroup->user`.`email` AS `UserGroup.user.email`, `UserGroup->user`.`role` AS `UserGroup.user.role`, `UserGroup->user`.`lastLoggedIn` AS `UserGroup.user.lastLoggedIn`, `UserGroup->user`.`appIdentifier` AS `UserGroup.user.appIdentifier`, `UserGroup->user`.`profilePictureURL` AS `UserGroup.user.profilePictureURL`, `UserGroup->user`.`socialId` AS `UserGroup.user.socialId`, `UserGroup->user`.`acceptedTerms` AS `UserGroup.user.acceptedTerms`, `UserGroup->user`.`socialAuthType` AS `UserGroup.user.socialAuthType`, `UserGroup->user`.`isBanned` AS `UserGroup.user.isBanned`, `UserGroup->user`.`isSuspended` AS `UserGroup.user.isSuspended`, `UserGroup->user`.`suspendedUntil` AS `UserGroup.user.suspendedUntil`, `UserGroup->user`.`coordinates` AS `UserGroup.user.coordinates`, `UserGroup->user`.`reasonRejected` AS `UserGroup.user.reasonRejected`, `UserGroup->user`.`profilePictureKey` AS `UserGroup.user.profilePictureKey`, `UserGroup->user`.`facebookGroupIds` AS `UserGroup.user.facebookGroupIds`, `UserGroup->user`.`facebookUserId` AS `UserGroup.user.facebookUserId`, `UserGroup->user`.`awdtsgFacebookUserId` AS `UserGroup.user.awdtsgFacebookUserId`, `UserGroup->user`.`activeGroup` AS `UserGroup.user.activeGroup`, `UserGroup->user`.`lastSeenNotification` AS `UserGroup.user.lastSeenNotification`, `UserGroup->user`.`rejectedGroupId` AS `UserGroup.user.rejectedGroupId`, `UserGroup->user`.`archived` AS `UserGroup.user.archived`, `UserGroup->user`.`createdAt` AS `UserGroup.user.createdAt`, `UserGroup->user`.`updatedAt` AS `UserGroup.user.updatedAt`, `UserGroup->user->groups`.`id` AS `UserGroup.user.groups.id`, `UserGroup->user->groups`.`city` AS `UserGroup.user.groups.city`, `UserGroup->user->groups`.`state` AS `UserGroup.user.groups.state`, `UserGroup->user->groups`.`country` AS `UserGroup.user.groups.country`, `UserGroup->user->groups`.`zipCode` AS `UserGroup.user.groups.zipCode`, `UserGroup->user->groups`.`latitude` AS `UserGroup.user.groups.latitude`, `UserGroup->user->groups`.`longitude` AS `UserGroup.user.groups.longitude`, `UserGroup->user->groups`.`milesRange` AS `UserGroup.user.groups.milesRange`, `UserGroup->user->groups`.`facebookGroupId` AS `UserGroup.user.groups.facebookGroupId`, `UserGroup->user->groups`.`createdAt` AS `UserGroup.user.groups.createdAt`, `UserGroup->user->groups`.`updatedAt` AS `UserGroup.user.groups.updatedAt`, `UserGroup->user->groups->UserGroup`.`id` AS `UserGroup.user.groups.UserGroup.id`, `UserGroup->user->groups->UserGroup`.`userId` AS `UserGroup.user.groups.UserGroup.userId`, `UserGroup->user->groups->UserGroup`.`groupId` AS `UserGroup.user.groups.UserGroup.groupId`, `UserGroup->user->groups->UserGroup`.`createdAt` AS `UserGroup.user.groups.UserGroup.createdAt`, `UserGroup->user->groups->UserGroup`.`updatedAt` AS `UserGroup.user.groups.UserGroup.updatedAt`, `UserGroup->user->permissions`.`id` AS `UserGroup.user.permissions.id`, `UserGroup->user->permissions`.`name` AS `UserGroup.user.permissions.name`, `UserGroup->user->permissions`.`description` AS `UserGroup.user.permissions.description`, `UserGroup->user->permissions`.`owner` AS `UserGroup.user.permissions.owner`, `UserGroup->user->permissions`.`admin` AS `UserGroup.user.permissions.admin`, `UserGroup->user->permissions`.`moderator` AS `UserGroup.user.permissions.moderator`, `UserGroup->user->permissions`.`user` AS `UserGroup.user.permissions.user`, `UserGroup->user->permissions`.`createdAt` AS `UserGroup.user.permissions.createdAt`, `UserGroup->user->permissions`.`updatedAt` AS `UserGroup.user.permissions.updatedAt`, `UserGroup->user->permissions->UserPermission`.`id` AS `UserGroup.user.permissions.UserPermission.id`, `UserGroup->user->permissions->UserPermission`.`userId` AS `UserGroup.user.permissions.UserPermission.userId`, `UserGroup->user->permissions->UserPermission`.`permissionId` AS `UserGroup.user.permissions.UserPermission.permissionId`, `UserGroup->user->permissions->UserPermission`.`enabled` AS `UserGroup.user.permissions.UserPermission.enabled`, `UserGroup->user->groupRequest`.`id` AS `UserGroup.user.groupRequest.id`, `UserGroup->user->groupRequest`.`groupName` AS `UserGroup.user.groupRequest.groupName`, `UserGroup->user->groupRequest`.`userFirstName` AS `UserGroup.user.groupRequest.userFirstName`, `UserGroup->user->groupRequest`.`userLastName` AS `UserGroup.user.groupRequest.userLastName`, `UserGroup->user->groupRequest`.`userPictureKey` AS `UserGroup.user.groupRequest.userPictureKey`, `UserGroup->user->groupRequest`.`groupUrl` AS `UserGroup.user.groupRequest.groupUrl`, `UserGroup->user->groupRequest`.`accepted` AS `UserGroup.user.groupRequest.accepted`, `UserGroup->user->groupRequest`.`acceptedById` AS `UserGroup.user.groupRequest.acceptedById`, `UserGroup->user->groupRequest`.`acceptedAt` AS `UserGroup.user.groupRequest.acceptedAt`, `UserGroup->user->groupRequest`.`userId` AS `UserGroup.user.groupRequest.userId`, `UserGroup->user->groupRequest`.`groupId` AS `UserGroup.user.groupRequest.groupId`, `UserGroup->user->groupRequest`.`createdAt` AS `UserGroup.user.groupRequest.createdAt`, `UserGroup->user->groupRequest`.`updatedAt` AS `UserGroup.user.groupRequest.updatedAt`, `UserGroup->user->rejectedGroup`.`id` AS `UserGroup.user.rejectedGroup.id`, `UserGroup->user->rejectedGroup`.`city` AS `UserGroup.user.rejectedGroup.city`, `UserGroup->user->rejectedGroup`.`state` AS `UserGroup.user.rejectedGroup.state`, `UserGroup->user->rejectedGroup`.`country` AS `UserGroup.user.rejectedGroup.country`, `UserGroup->user->rejectedGroup`.`zipCode` AS `UserGroup.user.rejectedGroup.zipCode`, `UserGroup->user->rejectedGroup`.`latitude` AS `UserGroup.user.rejectedGroup.latitude`, `UserGroup->user->rejectedGroup`.`longitude` AS `UserGroup.user.rejectedGroup.longitude`, `UserGroup->user->rejectedGroup`.`milesRange` AS `UserGroup.user.rejectedGroup.milesRange`, `UserGroup->user->rejectedGroup`.`facebookGroupId` AS `UserGroup.user.rejectedGroup.facebookGroupId`, `UserGroup->user->rejectedGroup`.`createdAt` AS `UserGroup.user.rejectedGroup.createdAt`, `UserGroup->user->rejectedGroup`.`updatedAt` AS `UserGroup.user.rejectedGroup.updatedAt` FROM `Users` AS `User` LEFT OUTER JOIN ( `UserGroups` AS `groups->UserGroup` INNER JOIN `Groups` AS `groups` ON `groups`.`id` = `groups->UserGroup`.`groupId`) ON `User`.`id` = `groups->UserGroup`.`userId` LEFT OUTER JOIN ( `UserPermissions` AS `permissions->UserPermission` INNER JOIN `Permissions` AS `permissions` ON `permissions`.`id` = `permissions->UserPermission`.`permissionId`) ON `User`.`id` = `permissions->UserPermission`.`userId` LEFT OUTER JOIN `UserGroupRequests` AS `groupRequest` ON `User`.`id` = `groupRequest`.`userId` LEFT OUTER JOIN `Groups` AS `rejectedGroup` ON `User`.`rejectedGroupId` = `rejectedGroup`.`id` INNER JOIN `UserGroups` AS `UserGroup` ON `User`.`id` = `UserGroup`.`userId` AND `UserGroup`.`groupId` = 52 LEFT OUTER JOIN `Users` AS `UserGroup->user` ON `UserGroup`.`userId` = `UserGroup->user`.`id` LEFT OUTER JOIN ( `UserGroups` AS `UserGroup->user->groups->UserGroup` INNER JOIN `Groups` AS `UserGroup->user->groups` ON `UserGroup->user->groups`.`id` = `UserGroup->user->groups->UserGroup`.`groupId`) ON `UserGroup->user`.`id` = `UserGroup->user->groups->UserGroup`.`userId` LEFT OUTER JOIN ( `UserPermissions` AS `UserGroup->user->permissions->UserPermission` INNER JOIN `Permissions` AS `UserGroup->user->permissions` ON `UserGroup->user->permissions`.`id` = `UserGroup->user->permissions->UserPermission`.`permissionId`) ON `UserGroup->user`.`id` = `UserGroup->user->permissions->UserPermission`.`userId` LEFT OUTER JOIN `UserGroupRequests` AS `UserGroup->user->groupRequest` ON `UserGroup->user`.`id` = `UserGroup->user->groupRequest`.`userId` LEFT OUTER JOIN `Groups` AS `UserGroup->user->rejectedGroup` ON `UserGroup->user`.`rejectedGroupId` = `UserGroup->user->rejectedGroup`.`id` WHERE (`User`.`id` != %s) HAVING `blockedUserCount` = 0 ORDER BY `User`.`updatedAt` DESC, `User`.`createdAt` DESC
        """
        params = (367183, 367183)  # 使用占位符绑定参数
        start_time = time.time()
        try:
            self.cursor.execute(query, params)
            self.cursor.fetchall()  # 获取所有结果集
            self.db.commit()  # 确保事务提交
            self.environment.events.request.fire(
                request_type="SQL",
                name="query2_data",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                success=True,  # 表示请求成功
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="SQL",
                name="query2_data",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                exception=e,
                success=False,  # 表示请求失败
            )
    

    def on_stop(self):
        """关闭连接"""
        try:
            # 清空所有未处理的结果集
            while self.cursor.nextset():
                pass
            self.cursor.close()
            self.db.close()
        except mysql.connector.Error as e:
            print(f"关闭连接时出错: {e}")


if __name__=='__main__':
   users = 1
   spawn_rate = 1
   run_time = "5s"
   report_path = "/Users/admin/Documents/projects/locust/locust/results/sqlreport.html"
   os.system(f'/Users/admin/Documents/projects/locust/locust/.venv/bin/locust -f {__file__}  -u {users} -r {spawn_rate} -t {run_time} --html {report_path} --web-port 8090')
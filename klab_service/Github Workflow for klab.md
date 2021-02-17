# Github Workflow Guide for klab

When you develop scripts with other group members, it is convenient to use github for version control and collaboration. The case is, people are usually responsible for a small part of the project. Therefore, it is common that the script you are working at have just been updated by others. If you notice this situation, it would cost much time to manually update others' modification at first before you publish your updates. If you are not able to notice it, maybe it will cover others' contributions to the script. Moreover, if there are still bugs or your codes don't fit with the logic of the project, it may destroy the whole project simply by pulling your scripts with same filenames into the shared folder. Therefore, it is very important to understand how to use github to do version control and make a guide for everyone to follow in order to avoid situations described above. So here is a suggestion about the scripts/software workflow for klab. Please take a look before you collaborate with others on some projects that need to do version control. Here, I will mainly focus on git command line usage on MacOS. If you don't have git installed, please refer to this [guide: installation for git](https://gist.github.com/derhuerst/1b15ff4652a867391f03).

## Work on a private repository

Although we will finally add our scripts to Rosetta Community, it is wise to first develop your scripts together in other place to make sure it works and is refined before uploaded to Rosetta Community. So the administrator/the main project manager could create a private repository under his/her account and invite colllaborators to the repository. 

The main procedure would be:

* 1. Go to your github account, [](github.com), create a new repository on the left top of the page, 

     ![image-20200723181727243](/Users/cplu/Library/Application Support/typora-user-images/image-20200723181727243.png)

     name your repository, such as **'covid-19'**, and set the repository as private,

     <img src="/Users/cplu/Library/Application Support/typora-user-images/image-20200723181934372.png" alt="image-20200723181934372" style="zoom:100%;" />

* 2. Go the your newly created repository, choose 'Settings'>'Manage access'>'Invite a collaborator' to add your collaborators by searching their github name or email,

     ![image-20200728123617000](/Users/cplu/Library/Application Support/typora-user-images/image-20200728123617000.png)

     For other collaborators, wait for your administrator to invite you.

* 3. Open your terminal on your local computer, go to the folder that you want to save and update your project.

     * For admin, create a new folder the same name as your repository:

       ```bash
       mkdir covid-19
       ```

       initialize it using git and link this folder with your remote repository:

       ```bash
       git init
       git remote add origin <url-for-your-just-created-repository>
       ```

     * For collaborators, clone the repository to your local computer:

       ```bash
       git clone <url-repository-you-want-to-clone>
       ```

## Version Control

After you clone or create a repository to your local computer, what is the right way to do version control is the next thing needed to be considered. Here, I recommend a way to not only keep tracking your updates and others' updates, but also having developing as well as latest developed version locally. This is suitable for either collaborators or administrators.

* 1. Before you start to develop the project, create a new branch called <your-username>/git-activity and then switch to that branch, for example:

  ```bash
  git checkout -b Nucleus2014/mutation
  ```

  Use git branch to check which branch you are at:

  ```bash
  git branch
  # Output: the branch labeled "*" is the branch you are at
  # * local
  # 	master
  ```

  For collaborators, additional actions are needed. Use push to tell github about your local branch,

  ```bash
  git push origin <username>/git-activity
  ```

  then Tell your local repository that it can pull from the copy of the branch on Github,

  ```bash
  git branch --set-upstream-to origin/<username>/git_activity
  ```

  

* 2. When you are satisfied with the development and would like to save a snapshot for your development, you could use add and commit to local branch:

  ```bash
  git add <files-have-been-developed>
  git commit -m "<comments-for-your-development>"
  ```

  You could add and commit several times to local branch anytime you want. These changes will not influence master branch.

* 3. When you think it is ready to share with others, 

     switch to master branch first:

     ```bash
     git checkout master
     ```

     fetch and merge remote changes by others: (**This step is very important. Please do it everytime before you rebase and push.**)

     ```bash
     git pull origin master
     ```

  * 3.1 For those **administrators**, (collaborators should be **cautious** to try this)

    Concatenate local branch after master branch:

    ```bash
    git rebase master Nucleus2014/mutation
    ```

    Push local branch to remote master branch:

    ```bash
    git push origin Nucleus2014/mutation:master
    ```

  * 3.2 For those **collaborators**,

    update your development to the remote branch called <your-username>/git-activity:

    ```bash
    git push origin <username>/git_activity
    ```

* 4. Return to local branch and do development further, repeat step 2 and step 3.

* 5. **Collaborators**: Go back to the github page of your repository, apply for "pull request" to let admins review your codes and decide whether to add into master branch or not.

     ![image-20200723191913182](/Users/cplu/Library/Application Support/typora-user-images/image-20200723191913182.png)

  NOTE: Always pull before push! It would be better pull again before you start to develop on the local branch next time. When you pull, local master branch will be synced with local and remote codes.

## Work on klab branch on RosettaCommons/main

When you would like submit finalized codes on RosettaCommons/main, it is similar with above steps mentioned for collaborators. However, one difference is that, in the private repository, you create the branch which is just updated by yourself, so there is no conflicts that will happen for your branch. For klab branch in RosettaCommons/main, all lab members could push, so before push to the branch, you need to pull first. 

If you never link the remote branch, 

first create a klab branch locally,

```bash
git checkout -b klab
```

create the link to the remote klab branch,

```bash
git branch --set-upstream-to origin/klab
```

then pull from the remote first,

```bash
git pull origin klab
```

then add and commit and push your **finalized** script,

```bash
git add <script>
git commit -m "<comment>"
git push origin klab
```

## Note

Once you are familiar with git workflow, you could work on RosettaCommon/main klab directly without creating private repository. However, I don't suggest you to do that, because there is little tolerance for you to have mistakes when you work on a branch that all lab members could edit without notice. In the future, there will be many well-built projects on it, and klab branch is more like a 'sub-master' branch of Rosetta rather than just a 'developing branch', that everyone in the lab should take care of.

### More resources for learning github

* If you would like to learn github quickly and interactively, I recommend [git-it](https://github.com/jlord/git-it-electron), which is a software developed by jlord

  ![screen shot 2016-04-17 at 10 37 55 pm](https://cloud.githubusercontent.com/assets/1305617/14594613/23873f64-04ed-11e6-9d3b-72f424dd0842.png)

* If you would like to learn github intensively and systematically, I recommend [Pro Git Book](https://git-scm.com/book/en/v2), written by Scott Chacon and Ben Straub and published by Apress. You could freely download using buttons on the right.

* Official Documentation is the best for you to quick search for commands usage: [Github Documentation](https://docs.github.com/en/github/using-git).

* If you would like to learn github with many clean charts and diagrams, especially know about different workflows on github, please refer to [atlassian Git Tutorials](https://www.atlassian.com/git/tutorials/comparing-workflows)

# Reference

1. Rosetta C++ Bootcamp in Feburary 2020 resources: **Lab 1: Introduction to Git** 
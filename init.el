;;; init.el --- Load the full configuration -*- lexical-binding: t -*-
;;; Commentary:

;; This file bootstraps the configuration, which is divided into
;; a number of other files.

;;; Code:

(let ((minver "25.1"))
  (when (version< emacs-version minver)
    (error "Your Emacs is too old -- this config requires v%s or higher" minver)))
(when (version< emacs-version "26.1")
  (message "Your Emacs is old, and some functionality in this config will be disabled. Please upgrade if possible."))

(add-to-list 'load-path (expand-file-name "lisp" user-emacs-directory)) ; 设定源码加载路径
;; (require 'init-benchmarking) ;; Measure startup time

(defconst *spell-check-support-enabled* nil) ;; Enable with t if you prefer
(defconst *is-a-mac* (eq system-type 'darwin))

;; Adjust garbage collection thresholds during startup, and thereafter

(let ((normal-gc-cons-threshold (* 20 1024 1024))
      (init-gc-cons-threshold (* 128 1024 1024)))
  (setq gc-cons-threshold init-gc-cons-threshold)
  (add-hook 'emacs-startup-hook
            (lambda () (setq gc-cons-threshold normal-gc-cons-threshold))))

;; (defun hello-world()
;;   (interactive)
;;   (message "Hello, world!"))
;; (provide 'hello)

(setq confirm-kill-emacs #'yes-or-no-p)           ; 在关闭Emacs前询问是否确认关闭，防止误触
(electric-pair-mode t)                            ; 自动补全括号
(add-hook 'prog-mode-hook #'show-paren-mode)      ; 编程模式下光标在括号上时高亮另一个括号
(column-number-mode t)                            ; 在Mode line上显示列号
(global-auto-revert-mode t)                       ; 当另一个程序修改了文件时让Emacs及时刷新Buffer
(delete-selection-mode t)                         ; 选中文本后输入文本会替换文本
(setq inhibit-startup-message t)                  ; 关闭启动Emacs时的欢迎界面
(setq make-backup-files nil)                      ; 关闭文件自动备份
(add-hook 'prog-mode-hook #'hs-minor-mode)        ; 编程模式下可以折叠代码块
(global-display-line-numbers-mode 1)              ; 在Window显示行号
(tool-bar-mode -1)                                ; 关闭ToolBar - 熟练后可选
(when (display-graphic-p) (toggle-scroll-bar -1)) ; 图形界面关闭滚动条

;; 以下为可选
;;(savehist-mode 1)                                 ; 打开Buffer历史记录保存
(setq display-line-numbers-type 'relative)        ; 显示相对行号
(add-to-list 'default-frame-alist '(width . 118)) ; 设定启动图形界面时初始Frame宽度（字符数）
(add-to-list 'default-frame-alist '(height . 80)) ; 设定启动图形界面时初始Frame高度（字符数）

;; 配置快捷键
(global-set-key (kbd "RET") 'newline-and-indent)  ; 新起一行并缩进
(global-set-key (kbd "C-c '") 'comment-or-uncomment-region) ; 为选中的代码加注释/去注释

(defun next-ten-lines()
  "Move cursor to next 10 lines."
  (interactive)
  (next-line 10))
(global-set-key (kbd "M-n") 'next-ten-lines)

(defun previous-ten-lines()
  "Move cursor to previous 10 lines."
  (interactive)
  (previous-line 10))
(global-set-key (kbd "M-p") 'previous-ten-lines)

(global-set-key (kbd "C-j") nil)
(global-set-key (kbd "C-j C-k") 'kill-whole-line)

;; MELPA
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

;; (require 'package)
;; (setq package-archives '(("gnu"   . "http://mirrors.cloud.tencent.com/elpa/gnu/")
;; 			 ("melpa" . "http://mirrors.cloud.tencent.com/elpa/melpa")))
;; (package-initialize)

;; 插件设置 use-package
(eval-when-compile
  (require 'use-package))

;; 插件 - 功能优化类
;; ivy插件
(use-package counsel
  :ensure t)

(use-package ivy
  :ensure t                          ; 确认安装，如果没有安装过 ivy 就自动安装    
  :init                              ; 在加载插件前执行命令
  (ivy-mode 1)                       ; 启动 ivy-mode
  (counsel-mode 1)
  :config                            ; 自定义一些变量，相当于赋值语句 (setq xxx yyy)
  (setq ivy-use-virtual-buffers t)        ; 一些官网提供的固定配置
  (setq ivy-count-format "(%d/%d) ")
  (setq search-default-mode #'char-fold-to-regexp)
  :bind                              ; 以下为绑定快捷键
  (("C-s" . 'swiper-isearch)          ; 绑定快捷键 C-s 为 swiper-search，替换原本的搜索功能
   ;; ("M-x" . 'counsel-M-x)             ; 使用 counsel 替换命令输入，给予更多提示
   ;; ("C-x C-f" . 'counsel-find-file)   ; 使用 counsel 做文件打开操作，给予更多提示
   ;; ("M-y" . 'counsel-yank-pop)        ; 使用 counsel 做历史剪贴板粘贴，可以展示历史
   ("C-x b" . 'ivy-switch-buffer)     ; 使用 ivy 做 buffer 切换，给予更多提示
   ("C-c v" . 'ivy-push-view)         ; 记录当前 buffer 的信息
   ("C-c s" . 'ivy-switch-view)       ; 切换到记录过的 buffer 位置
   ("C-c V" . 'ivy-pop-view)          ; 移除 buffer 记录
   ("C-x C-SPC" . 'counsel-mark-ring) ; 使用 counsel 记录 mark 的位置
   ("<f1> f" . 'counsel-describe-function)
   ("<f1> v" . 'counsel-describe-variable)
   ("<f1> i" . 'counsel-info-lookup-symbol)
   :map minibuffer-local-map
   ("C-r" . counsel-minibuffer-history)))

;; amx - 记录M-x输入的命令历史
(use-package amx
  :ensure t
  :init (amx-mode))

;; ace-window Emacs多窗口使用编号切换
(use-package ace-window
  :ensure t
  :bind ("C-x o" . 'ace-window))

;; mwim 行首 文字首 行尾 文字尾切换
(use-package mwim
  :ensure t
  :bind
  ("C-a" . mwim-beginning-of-code-or-line)
  ("C-e" . mwim-end-of-code-or-line))

;; undo tree
(use-package undo-tree
  :ensure t
  :init (global-undo-tree-mode)
  :config (setq undo-tree-auto-save-history nil))

;; smart mode line (optional)
;; (use-package smart-mode-line
;;   :ensure t
;;   :init (sml/setup))

;; good scroll (optional)
(use-package good-scroll
  :ensure t
  :if window-system
  :init (good-scroll-mode))

;; 编程模式下代码语法检查
(use-package flycheck
 :ensure t
 :hook
 (prog-mode . flycheck-mode))


(provide 'init)
;;; init.el ends here


(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes
   '("a27c00821ccfd5a78b01e4f35dc056706dd9ede09a8b90c6955ae6a390eb1c1e" default))
 '(ispell-dictionary nil)
 '(package-selected-packages
   '(good-scroll smart-mode-line undo-tree mwim ace-window amx counsel ivy use-package)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

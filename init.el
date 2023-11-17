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
(add-to-list 'default-frame-alist '(width . 121)) ; 设定启动图形界面时初始Frame宽度（字符数）
(add-to-list 'default-frame-alist '(height . 65)) ; 设定启动图形界面时初始Frame高度（字符数）

;; 配置快捷键
(global-set-key (kbd "RET") 'newline-and-indent)  ; 新起一行并缩进
(global-set-key (kbd "C-c '") 'comment-or-uncomment-region) ; 为选中的代码加注释/去注释

(defun next-ten-lines()
  "Move cursor to next 10 lines."
  (interactive)
  (forward-line 10))
(global-set-key (kbd "M-n") 'next-ten-lines)

(defun previous-ten-lines()
  "Move cursor to previous 10 lines."
  (interactive)
  (forward-line -10))
(global-set-key (kbd "M-p") 'previous-ten-lines)

(global-set-key (kbd "C-j") nil)
(global-set-key (kbd "C-j C-k") 'kill-whole-line)

;; MELPA
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
;; Comment/uncomment this line to enable MELPA Stable if desired.  See `package-archive-priorities`
;; and `package-pinned-packages`. Most users will not need or want to do this.
;;(add-to-list 'package-archives '("melpa-stable" . "https://stable.melpa.org/packages/") t)
(package-initialize)

;; (require 'package)
;; (setq package-archives '(("gnu"   . "http://mirrors.cloud.tencent.com/elpa/gnu/")
;;        ("melpa" . "http://mirrors.cloud.tencent.com/elpa/melpa")))
;; (package-initialize)

;; 插件设置 use-package
(eval-when-compile
  (require 'use-package))

;; 插件 - 功能优化类 **********************************************************
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

;;hydra 组合特定场景的命令
(use-package hydra :ensure t)
(use-package use-package-hydra :ensure t :after hydra)

;; undo tree
(use-package undo-tree
  :ensure t
  :init (global-undo-tree-mode)
  :config (setq undo-tree-auto-save-history nil)
  :after hydra
  :bind ("C-x C-h u" . hydra-undo-tree/body)
  :hydra (hydra-undo-tree (:hint nil)
  "
  _p_: undo _n_: redo _s_: save _l_: load "
  ("p" undo-tree-undo)
  ("n" undo-tree-redo)
  ("s" undo-tree-save-history)
  ("l" undo-tree-load-history)
  ("u" undo-tree-visualize "visualize" :color blue)
  ("q" nil "quit" :color blue)))

;; smart mode line (optional)
(use-package smart-mode-line
  :ensure t
  :init
  (setq sml/no-confirm-load-theme t) ; avoid asking when startup
  (sml/setup)
  :config
  (setq rm-blacklist (format "^ \\(%s\\)$" (mapconcat #'identity
    '("Projectile.*" "company*" "Google" "Undo-Tree" "counsel" "ivy" "yas" "WK")
    "\\|"))))

;; good scroll (optional)
(use-package good-scroll
  :ensure t
  :if window-system
  :init (good-scroll-mode))

;; 插件 - 功增强类 ************************************************************
;; Book marks
;; C-x r m (bookmark-set)
;; C-x r b (bookmark-jump)
;; C-x r l (bookmark-bmenu-list)
;; M-x (bookmark-delete)

;; ivy view
;; C-c v (ivy-push-view)
;; C-c s (ivy-switch-view)
;; C-c V (ivy-pop-view)

;; which-key(optional)
(use-package which-key
  :ensure t
  :init (which-key-mode))

;; avy 无鼠标的光标跳转
(use-package avy
  :ensure t
  :config
  (defun avy-action-embark (pt)
      (unwind-protect (save-excursion (goto-char pt) (embark-act))
        (select-window (cdr (ring-ref avy-ring 0)))) t)
  (setf (alist-get ?e avy-dispatch-alist) 'avy-action-embark)
  :bind ("C-j C-SPC" . avy-goto-char-timer))

;; marginalia 为minibuffer中的选项添加注解
(use-package marginalia
  :ensure t
  :init (marginalia-mode)
  :bind (:map minibuffer-local-map ("M-A" . marginalia-cycle)))

;; embark (optional)
(use-package embark
  :ensure t

  :bind
  (("M-." . embark-act)         ;; pick some comfortable binding
   ("C-;" . embark-dwim)        ;; good alternative: M-.
   ("C-h B" . embark-bindings)) ;; alternative for `describe-bindings'

  :init

  ;; Optionally replace the key help with a completing-read interface
  (setq prefix-help-command #'embark-prefix-help-command)

  ;; Show the Embark target at point via Eldoc.  You may adjust the Eldoc
  ;; strategy, if you want to see the documentation from multiple providers.
  ;;(add-hook 'eldoc-documentation-functions #'embark-eldoc-first-target)
  ;; (setq eldoc-documentation-strategy #'eldoc-documentation-compose-eagerly)

  :config

  ;; Hide the mode line of the Embark live/completions buffers
  (add-to-list 'display-buffer-alist
               '("\\`\\*Embark Collect \\(Live\\|Completions\\)\\*"
                 nil
                 (window-parameters (mode-line-format . none)))))

;; Consult users will also want the embark-consult package.
(use-package embark-consult
  :ensure t ; only need to install it, embark loads it after consult if found
  :hook
  (embark-collect-mode . consult-preview-at-point-mode))

;;multiple cursors 多光标编辑
(use-package multiple-cursors
  :ensure t
  :after hydra
  :bind
  (("C-x C-h m" . hydra-multiple-cursors/body)
   ("C-S-c C-S-c" . mc/edit-lines)
   ("C->" . mc/mark-next-like-this)
   ("C-<" . mc/mark-previous-like-this)
   ("C-c C-<" . mc/mark-all-like-this)
  ("C-S-<mouse-1>" . mc/toggle-cursor-on-click))
  :hydra (hydra-multiple-cursors (:hint nil)
          "
Up^^             Down^^           Miscellaneous           % 2(mc/num-cursors) cursor%s(if (> (mc/num-cursors) 1) \"s\" \"\")
------------------------------------------------------------------
 [_p_]   Prev like this        [_n_]   Next like this        [_l_] Edit lines  [_0_] Insert numbers
 [_P_]   Skip prev like this   [_N_]   Skip next like this   [_a_] Mark all    [_A_] Insert letters
 [_M-p_] Unmark prev like this [_M-n_] Unmark next like this [_s_] Mark all in region regexp
 [_|_]   Align with input CHAR [Click] Cursor at point       [_q_] Quit"
    ("l" mc/edit-lines :exit t)
    ("a" mc/mark-all-like-this :exit t)
    ("n" mc/mark-next-like-this)
    ("N" mc/skip-to-next-like-this)
    ("M-n" mc/unmark-next-like-this)
    ("p" mc/mark-previous-like-this)
    ("P" mc/skip-to-previous-like-this)
    ("M-p" mc/unmark-previous-like-this)
    ("|" mc/vertical-align)
    ("s" mc/mark-all-in-region-regexp :exit t)
    ("0" mc/insert-numbers :exit t)
    ("A" mc/insert-letters :exit t)
    ("<mouse-1>" mc/add-cursor-on-click)
    ;; Help with click recognition in this hydra
    ("<down-mouse-1>" ignore)
    ("<drag-mouse-1>" ignore)
    ("q" nil)))

;; dashboard
(use-package dashboard
 :ensure t
 :config
 (setq dashboard-banner-logo-title "Welcome to Emacs!") ;; 个性签名，随读者喜好设置
 ;; (setq dashboard-projects-backend 'projectile) ;; 读者可以暂时注释掉这一行，等安装了 projectile 后再使用
 (setq dashboard-startup-banner 'official) ;; 也可以自定义图片
 (setq dashboard-items '((recents  . 5)   ;; 显示多少个最近文件
       (bookmarks . 5)  ;; 显示多少个最近书签
       (projects . 10))) ;; 显示多少个最近项目
 (dashboard-setup-startup-hook))

;; tiny tiny-expand 序号扩展
(use-package tiny :ensure t)

;; highlight symbol 高亮所有光标所在处的符号
(use-package highlight-symbol
  :ensure t
  :init (highlight-symbol-mode)
  :bind ("<f3>" . highlight-symbol))

;; rainbow delimiters 使用颜色标记多级括号
(use-package rainbow-delimiters
  :ensure t
  :hook (prog-mode . rainbow-delimiters-mode))

;; 插件 - 编程开发类 *********************************************************
;; 代码补全功能
(use-package company
  :ensure t
  :init (global-company-mode)
  :config
  (setq company-minimum-prefix-length 1)
  (setq company-tooltip-align-annotations t)
  (setq company-idle-delay 0.0)
  ;; (setq company-show-numbers t)
  (setq company-show-quick-access t)
  (setq company-selection-wrap-around t)
  (setq company-transformers '(company-sort-by-occurrence)))
;; UI 界面显示一个box
;; (use-package company-box
;;   :ensure t
;;   :if window-system
;;   :hook (company-mode . company-box-mode))

;; 文本展开
(global-set-key (kbd "M-/") 'hippie-expand)

;; 编程模式下代码语法检查
(use-package flycheck
  :ensure t
  :config (setq truncate-lines nil) ; 如果单行信息很长会自动换行
 :hook
 (prog-mode . flycheck-mode))

;; Language Server Protocol 代码分析 - 前端
(use-package lsp-mode
  :ensure t
  :init
  (setq lsp-keymap-prefix "C-c l" lsp-file-watch-threshold 500)
  :hook (lsp-mode . lsp-enable-which-key-integration) ;; which key integration
  :config
  ;;(setq lsp-completion-provider :none) ;; 阻止lsp重新设置company-backend而覆盖yasnippet的设置
  (setq lsp-headerline-breadcrumb-enable t)
  :bind ("C-c l s" . lsp-ivy-workspace-symbol)) ;; 可快速搜索工作区内的符号（类名、函数名、变量名等）

;; lsp ui
(use-package lsp-ui
  :ensure t
  :config
  (define-key lsp-ui-mode-map [remap xref-find-definitions] #'lsp-ui-peek-find-definitions)
  (define-key lsp-ui-mode-map [remap xref-find-references] #'lsp-ui-peek-find-references)
  (setq lsp-ui-doc-position 'top))

(use-package lsp-ivy :ensure t :after (lsp-mode))

;; 代码调试 Debug Adapter Protocol  前后端分离
(use-package dap-mode
  :ensure t
  :after hydra lsp-mode
  :commands dap-debug
  :custom (dap-auto-configure-mode t)
  :config (dap-ui-mode 1)
  :hydra (hydra-dap-mode (:color pink :hint nil :foreign-keys run)
			 "
^Stepping^          ^Switch^                 ^Breakpoints^         ^Debug^                     ^Eval
^^^^^^^^----------------------------------------------------------------------------------------------------------------
_n_: Next           _ss_: Session            _bb_: Toggle          _dd_: Debug                 _ee_: Eval
_i_: Step in        _st_: Thread             _bd_: Delete          _dr_: Debug recent          _er_: Eval region
_o_: Step out       _sf_: Stack frame        _ba_: Add             _dl_: Debug last            _es_: Eval thing at point
_c_: Continue       _su_: Up stack frame     _bc_: Set condition   _de_: Edit debug template   _ea_: Add expression.
_r_: Restart frame  _sd_: Down stack frame   _bh_: Set hit count   _ds_: Debug restart
_Q_: Disconnect     _sl_: List locals        _bl_: Set log message
                  _sb_: List breakpoints
                  _sS_: List sessions
"
   ("n" dap-next)
   ("i" dap-step-in)
   ("o" dap-step-out)
   ("c" dap-continue)
   ("r" dap-restart-frame)
   ("ss" dap-switch-session)
   ("st" dap-switch-thread)
   ("sf" dap-switch-stack-frame)
   ("su" dap-up-stack-frame)
   ("sd" dap-down-stack-frame)
   ("sl" dap-ui-locals)
   ("sb" dap-ui-breakpoints)
   ("sS" dap-ui-sessions)
   ("bb" dap-breakpoint-toggle)
   ("ba" dap-breakpoint-add)
   ("bd" dap-breakpoint-delete)
   ("bc" dap-breakpoint-condition)
   ("bh" dap-breakpoint-hit-condition)
   ("bl" dap-breakpoint-log-message)
   ("dd" dap-debug)
   ("dr" dap-debug-recent)
   ("ds" dap-debug-restart)
   ("dl" dap-debug-last)
   ("de" dap-debug-edit-template)
   ("ee" dap-eval)
   ("ea" dap-ui-expressions-add)
   ("er" dap-eval-region)
   ("es" dap-eval-thing-at-point)
   ("q" nil "quit" :color blue)
   ("Q" dap-disconnect :color red)))

;; 项目管理
(use-package projectile
  :ensure t
  :bind ("C-c p" . projectile-command-map)
  :config
  (setq projectile-mode-line "Projectile")
  (setq projectile-track-know-projects-automatically nil))

(use-package counsel-projectile
  :ensure t
  :after (projectile)
  :init (counsel-projectile-mode))

;; 版本管理
(use-package magit :ensure t)

;; C++ lsp后端
(use-package c++-mode
  :functions c-toggle-hungry-state ;; 按下删除键时尽可能多的删除空白字符
  :hook
  (c-mode . lsp-deferred)
  (c++-mode . lsp-deferred)
  (c++-mode . c-toggle-hungry-state))

;; C++ dap后端
(use-package dap-lldb
  :after dap-mode
  :custom (dap-lldb-debug-program '("lldb-vscode"))
  (dap-lldb-debugged-program-function (lambda () (read-file-name "Select file to debug: "))))

;; python lsp后端
(use-package python
  :defer t
  :mode ("\\.py\\'" . python-mode)
  :interpreter ("python" . python-mode)
  :config (require 'dap-python)) ;; for debug
;; M-x pyvenv-workon -> to find all miniconda envs
(use-package pyvenv
  :ensure t
  :config (setenv "WORKON_HOME" (expand-file-name "C:\\Users\\Jack\\scoop\\persist\\miniconda3\\envs"))
  ;;:config (setenv "WORKON_HOME" (expand-file-name "~/scoop/persist/miniconda3/envs"))
  (pyvenv-mode t))
  ;;:hook (python-mode . (lambda () (pyvenv-workon "..")))) ;; 启动后激活miniconda base env

;; lsp后端
(use-package lsp-pyright
  :ensure t
  :config
  :hook (python-mode . (lambda () (require 'lsp-pyright) (lsp-deferred))))

;; noetree theme
(setq neo-theme (if (display-graphic-p) 'icons 'arrow))

(use-package neotree
  :ensure t
  :after projectile
  :config
  (setq neo-smart-open t)
  ;; when running projectile switch project action neotree will change root automatically
  (setq projectile-switch-project-action 'neotree-projectile-action))

(defun neotree-project-dir()
    "Open NeoTree using the git root."
    (interactive)
    (let ((project-dir (projectile-project-root))
	  (file-name (buffer-file-name)))
      (neotree-toggle)
      (if project-dir (if (neo-global--window-exists-p)
			  (progn (neotree-dir project-dir) (neotree-find file-name)))
	(message "Could not find git project root."))))
(global-set-key [f8] 'neotree-project-dir)
;;(global-set-key (kbd "<f8>") 'neotree-project-dir)

;; Themes
(load-theme 'dracula t)

(use-package all-the-icons
  :if (display-graphic-p))

(provide 'init)
;;; init.el ends here
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(column-number-mode t)
 '(custom-safe-themes
   '("603a831e0f2e466480cdc633ba37a0b1ae3c3e9a4e90183833bc4def3421a961" default))
 '(display-line-numbers-type 'relative)
 '(global-display-line-numbers-mode t)
 '(ispell-dictionary nil)
 '(package-selected-packages
   '(lsp-pyright pyvenv python-mode magit counsel-projectile dap-mode lsp-ivy lsp-ui lsp-mode company-tabnine company-box projectile company all-the-icons tiny cmake-mode which-key use-package-hydra undo-tree swiper-helm smart-mode-line rainbow-delimiters mwim multiple-cursors marginalia ivy-avy hydra highlight-symbol good-scroll flycheck embark dashboard counsel amx ace-window))
 '(tool-bar-mode nil))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:family "SauceCodePro NFM" :foundry "outline" :slant normal :weight regular :height 110 :width normal)))))

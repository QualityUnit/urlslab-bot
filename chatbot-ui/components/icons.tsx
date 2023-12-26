import {
  LucideProps,
  Moon,
  SunMedium,
  Twitter,
  type Icon as LucideIcon,
} from "lucide-react"

export type Icon = LucideIcon

export const Icons = {
  sun: SunMedium,
  moon: Moon,
  twitter: Twitter,
  logo: (props: LucideProps) => (
      <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
              d="M22.8277 22.3183C22.8277 25.532 20.2135 28.1463 16.9998 28.1463C13.7861 28.1463 11.1718 25.532 11.1718 22.3183C11.1693 21.5404 11.3237 20.7699 11.626 20.053C11.9282 19.3361 12.3719 18.6876 12.9307 18.1462C13.125 17.9612 13.3845 17.8602 13.6529 17.8651C13.9212 17.8701 14.1768 17.9806 14.3642 18.1728C14.5516 18.3649 14.6557 18.6232 14.6539 18.8915C14.6522 19.1599 14.5448 19.4168 14.3549 19.6065C13.8157 20.1324 13.4455 20.8071 13.2917 21.5445C13.1378 22.2818 13.2073 23.0483 13.4912 23.7459C13.7751 24.4436 14.2605 25.0408 14.8855 25.4612C15.5105 25.8816 16.2466 26.1061 16.9998 26.1061C17.753 26.1061 18.4891 25.8816 19.1141 25.4612C19.739 25.0408 20.2245 24.4436 20.5084 23.7459C20.7923 23.0483 20.8617 22.2818 20.7079 21.5445C20.554 20.8071 20.1838 20.1324 19.6446 19.6065C19.4548 19.4168 19.3474 19.1599 19.3456 18.8915C19.3439 18.6232 19.448 18.3649 19.6354 18.1728C19.8228 17.9806 20.0784 17.8701 20.3467 17.8651C20.615 17.8602 20.8745 17.9612 21.0689 18.1462C21.6276 18.6876 22.0714 19.3361 22.3736 20.053C22.6758 20.7699 22.8303 21.5404 22.8277 22.3183ZM18.0198 20.7346V13.2662C18.0198 12.9957 17.9123 12.7362 17.721 12.5449C17.5297 12.3537 17.2703 12.2462 16.9998 12.2462C16.7293 12.2462 16.4698 12.3537 16.2785 12.5449C16.0872 12.7362 15.9798 12.9957 15.9798 13.2662V20.7346C15.9798 21.0052 16.0872 21.2646 16.2785 21.4559C16.4698 21.6472 16.7293 21.7546 16.9998 21.7546C17.2703 21.7546 17.5297 21.6472 17.721 21.4559C17.9123 21.2646 18.0198 21.0052 18.0198 20.7346ZM23.7294 8.40453C23.6398 8.24938 23.511 8.12055 23.3558 8.03102C23.2006 7.94149 23.0246 7.89442 22.8454 7.89453L11.1535 7.89453C10.9744 7.89442 10.7984 7.94146 10.6432 8.03094C10.4881 8.12042 10.3592 8.24917 10.2696 8.40425C10.18 8.55933 10.1328 8.73527 10.1328 8.91437C10.1328 9.09347 10.1799 9.26942 10.2695 9.42453L12.7593 13.7364C12.8946 13.9709 13.1174 14.142 13.3788 14.2121C13.6403 14.2823 13.9188 14.2457 14.1533 14.1104C14.3877 13.9752 14.5589 13.7523 14.629 13.4909C14.6991 13.2294 14.6626 12.9509 14.5273 12.7164L12.9198 9.93453H21.0798L19.4733 12.7164C19.4063 12.8325 19.3629 12.9606 19.3454 13.0935C19.328 13.2264 19.3369 13.3614 19.3716 13.4909C19.4063 13.6203 19.4662 13.7417 19.5478 13.848C19.6294 13.9543 19.7312 14.0434 19.8473 14.1104C19.9634 14.1774 20.0915 14.2208 20.2244 14.2383C20.3573 14.2557 20.4923 14.2468 20.6217 14.2121C20.7512 14.1774 20.8725 14.1175 20.9788 14.0359C21.0851 13.9543 21.1743 13.8525 21.2413 13.7364L23.7308 9.42487C23.8202 9.26965 23.8671 9.09363 23.8668 8.91452C23.8666 8.7354 23.8192 8.55951 23.7294 8.40453Z"
              fill="white"/>
      </svg>
  ),
    gitHub: (props: LucideProps) => (
        <svg viewBox="0 0 438.549 438.549" {...props}>
            <path
                fill="currentColor"
                d="M409.132 114.573c-19.608-33.596-46.205-60.194-79.798-79.8-33.598-19.607-70.277-29.408-110.063-29.408-39.781 0-76.472 9.804-110.063 29.408-33.596 19.605-60.192 46.204-79.8 79.8C9.803 148.168 0 184.854 0 224.63c0 47.78 13.94 90.745 41.827 128.906 27.884 38.164 63.906 64.572 108.063 79.227 5.14.954 8.945.283 11.419-1.996 2.475-2.282 3.711-5.14 3.711-8.562 0-.571-.049-5.708-.144-15.417a2549.81 2549.81 0 01-.144-25.406l-6.567 1.136c-4.187.767-9.469 1.092-15.846 1-6.374-.089-12.991-.757-19.842-1.999-6.854-1.231-13.229-4.086-19.13-8.559-5.898-4.473-10.085-10.328-12.56-17.556l-2.855-6.57c-1.903-4.374-4.899-9.233-8.992-14.559-4.093-5.331-8.232-8.945-12.419-10.848l-1.999-1.431c-1.332-.951-2.568-2.098-3.711-3.429-1.142-1.331-1.997-2.663-2.568-3.997-.572-1.335-.098-2.43 1.427-3.289 1.525-.859 4.281-1.276 8.28-1.276l5.708.853c3.807.763 8.516 3.042 14.133 6.851 5.614 3.806 10.229 8.754 13.846 14.842 4.38 7.806 9.657 13.754 15.846 17.847 6.184 4.093 12.419 6.136 18.699 6.136 6.28 0 11.704-.476 16.274-1.423 4.565-.952 8.848-2.383 12.847-4.285 1.713-12.758 6.377-22.559 13.988-29.41-10.848-1.14-20.601-2.857-29.264-5.14-8.658-2.286-17.605-5.996-26.835-11.14-9.235-5.137-16.896-11.516-22.985-19.126-6.09-7.614-11.088-17.61-14.987-29.979-3.901-12.374-5.852-26.648-5.852-42.826 0-23.035 7.52-42.637 22.557-58.817-7.044-17.318-6.379-36.732 1.997-58.24 5.52-1.715 13.706-.428 24.554 3.853 10.85 4.283 18.794 7.952 23.84 10.994 5.046 3.041 9.089 5.618 12.135 7.708 17.705-4.947 35.976-7.421 54.818-7.421s37.117 2.474 54.823 7.421l10.849-6.849c7.419-4.57 16.18-8.758 26.262-12.565 10.088-3.805 17.802-4.853 23.134-3.138 8.562 21.509 9.325 40.922 2.279 58.24 15.036 16.18 22.559 35.787 22.559 58.817 0 16.178-1.958 30.497-5.853 42.966-3.9 12.471-8.941 22.457-15.125 29.979-6.191 7.521-13.901 13.85-23.131 18.986-9.232 5.14-18.182 8.85-26.84 11.136-8.662 2.286-18.415 4.004-29.263 5.146 9.894 8.562 14.842 22.077 14.842 40.539v60.237c0 3.422 1.19 6.279 3.572 8.562 2.379 2.279 6.136 2.95 11.276 1.995 44.163-14.653 80.185-41.062 108.068-79.226 27.88-38.161 41.825-81.126 41.825-128.906-.01-39.771-9.818-76.454-29.414-110.049z"
            ></path>
        </svg>
    ),
}
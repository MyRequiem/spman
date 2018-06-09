#!/bin/bash

_spman() {
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    subcommands_main="--help --check-version --repolist --repoinfo --blacklist \
        --update --health --new-config --check-upgrade --download \
        --upgrade-pkgs --remove-pkgs --queue --find-deps --view-slackbuild \
        --find-pkg --check-deps --bad-links --pkglist"
    subcommands_download="--pkg --src"
    subcommands_repo_pkg="alienbob multilib slack"
    subcommands_repo_src="alienbob sbo slack"
    subcommands_queue="--add --remove --clear --show --install"
    subcommands_check_deps="--sbbdep --ldd"
    subcommands_pkglist="alienbob multilib sbo slack"

    if [[ ${COMP_CWORD} == 1 ]] ; then
        COMPREPLY=($(compgen -W "${subcommands_main}" -- "${cur}"))
        return 0
    fi

    case "${COMP_WORDS[1]}" in
        --help|--check-version|--repolist|--repoinfo|--blacklist|--update|\
            --health|--new-config|--check-upgrade|--remove-pkgs)
            COMPREPLY=()
            return 0
            ;;

        -d|--download)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_download}" -- "${cur}"))
                return 0
            fi

            if [[ ${COMP_CWORD} == 3 ]] ; then
                case "${COMP_WORDS[2]}" in
                    --pkg)
                        COMPREPLY=($(compgen -W "${subcommands_repo_pkg}" -- "${cur}"))
                        ;;

                    --src)
                        COMPREPLY=($(compgen -W "${subcommands_repo_src}" -- "${cur}"))
                        ;;
                esac
                return 0
            fi

            if [[ ${COMP_CWORD} == 4 ]] ; then
                COMPREPLY=($(compgen -W "pkgList" -- "${cur}"))
                return 0
            fi
            ;;

        -m|--upgrade-pkgs)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "--only-new" -- "${cur}"))
                return 0
            fi
            ;;

        -q|--queue)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_queue}" -- "${cur}"))
                return 0
            fi

            case "${COMP_WORDS[2]}" in
                --add|--remove)
                    if [[ ${COMP_CWORD} == 3 ]] ; then
                        COMPREPLY=($(compgen -W "pkgList" -- "${cur}"))
                        return 0
                    fi
                    ;;

                --clear|--show|--install)
                    COMPREPLY=()
                    return 0
                    ;;
            esac
            ;;

        -p|--find-deps)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "pkgName" -- "${cur}"))
                return 0
            fi
            ;;

        -s|--view-slackbuild)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "pkgName" -- "${cur}"))
                return 0
            fi
            ;;

        -f|--find-pkg)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "--strict" -- "${cur}"))
                return 0
            fi

            if [[ ${COMP_CWORD} == 3 ]] ; then
                COMPREPLY=($(compgen -W "pkgName" -- "${cur}"))
                return 0
            fi
            ;;

        -i|--pkglist)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_pkglist}" -- "${cur}"))
                return 0
            fi

            if [[ ${COMP_CWORD} == 3 ]] ; then
                COMPREPLY=($(compgen -W "--only-installed" -- "${cur}"))
                return 0
            fi
            ;;

        -k|--check-deps)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_check_deps}" -- "${cur}"))
                return 0
            fi
            ;;

        -a|--bad-links)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=($(compgen -d -- "${cur}"))
                return 0
            fi
            ;;
    esac

    return 0
}

complete -F _spman spman

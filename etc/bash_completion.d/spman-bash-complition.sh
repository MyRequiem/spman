_spman() {
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    subcommands_main="--help --check-version --repolist --repoinfo --blacklist \
        --update --health --new-config --check-upgrade --download --queue \
        --find-deps --view-slackbuild --find-pkg"

    subcommands_download="--pkg --src"
    subcommands_repo_pkg="alienbob multilib slack"
    subcommands_repo_src="alienbob sbo slack"
    subcommands_pkgname="pkg(s)"
    subcommands_queue="--add --remove --clear --show --install"
    subcommands_find_deps="pkg"

    if [[ ${COMP_CWORD} == 1 ]] ; then
        COMPREPLY=( $(compgen -W "${subcommands_main}" -- ${cur}) )
        return 0
    fi

    case "${COMP_WORDS[1]}" in
        --help|--check-version|--repolist|--repoinfo|--blacklist|--update|\
            --health|--new-config|--check-upgrade)
            COMPREPLY=()
            return 0
            ;;

        --download)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=( $(compgen -W "${subcommands_download}" -- ${cur}) )
                return 0
            fi

            if [[ ${COMP_CWORD} == 3 ]] ; then
                case "${COMP_WORDS[2]}" in
                    --pkg)
                        COMPREPLY=($(compgen -W "${subcommands_repo_pkg}" -- ${cur}))
                        ;;

                    --src)
                        COMPREPLY=($(compgen -W "${subcommands_repo_src}" -- ${cur}))
                        ;;
                esac
                return 0
            fi

            if [[ ${COMP_CWORD} == 4 ]] ; then
                COMPREPLY=($(compgen -W "${subcommands_pkgname}" -- ${cur}))
                return 0
            fi
            ;;

        --queue)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=( $(compgen -W "${subcommands_queue}" -- ${cur}) )
                return 0
            fi

            case "${COMP_WORDS[2]}" in
                --add|--remove)
                    if [[ ${COMP_CWORD} == 3 ]] ; then
                        COMPREPLY=($(compgen -W "${subcommands_pkgname}" -- ${cur}))
                        return 0
                    fi
                    ;;

                --clear|--show|--install)
                    COMPREPLY=()
                    return 0
                    ;;
            esac
            ;;

        --find-deps|--view-slackbuild|--find-pkg)
            if [[ ${COMP_CWORD} == 2 ]] ; then
                COMPREPLY=( $(compgen -W "${subcommands_find_deps}" -- ${cur}) )
                return 0
            fi
            ;;
    esac

    return 0
}

complete -F _spman spman

